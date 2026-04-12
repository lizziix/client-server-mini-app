import pytest
from playwright.sync_api import Page, expect


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def open_app(page: Page, base_url: str) -> None:
    page.goto(base_url)
    # Ждём, пока таблица загрузится (JS сделал fetch)
    expect(page.get_by_test_id("products-body").locator("tr").first).to_be_visible()


def fill_add_form(page: Page, id_: int, name: str, price: float) -> None:
    page.get_by_test_id("input-id").fill(str(id_))
    page.get_by_test_id("input-name").fill(name)
    page.get_by_test_id("input-price").fill(str(price))
    page.get_by_test_id("btn-add").click()


# ---------------------------------------------------------------------------
# Page load
# ---------------------------------------------------------------------------

class TestPageLoad:
    def test_page_title(self, page: Page, base_url: str):
        page.goto(base_url)
        expect(page).to_have_title("Products")

    def test_table_is_visible(self, page: Page, base_url: str):
        page.goto(base_url)
        expect(page.get_by_test_id("products-table")).to_be_visible()

    def test_add_form_is_visible(self, page: Page, base_url: str):
        page.goto(base_url)
        expect(page.get_by_test_id("add-form")).to_be_visible()

    def test_modal_is_hidden_on_load(self, page: Page, base_url: str):
        page.goto(base_url)
        expect(page.get_by_test_id("modal-overlay")).to_be_hidden()


# ---------------------------------------------------------------------------
# Product list
# ---------------------------------------------------------------------------

class TestProductList:
    def test_initial_products_count(self, page: Page, base_url: str):
        open_app(page, base_url)
        rows = page.get_by_test_id("products-body").locator("tr")
        expect(rows).to_have_count(2)

    def test_milk_shown(self, page: Page, base_url: str):
        open_app(page, base_url)
        expect(page.get_by_test_id("cell-name-1")).to_have_text("Milk")

    def test_bread_shown(self, page: Page, base_url: str):
        open_app(page, base_url)
        expect(page.get_by_test_id("cell-name-2")).to_have_text("Bread")

    def test_price_is_displayed(self, page: Page, base_url: str):
        open_app(page, base_url)
        expect(page.get_by_test_id("cell-price-1")).to_have_text("89.90")


# ---------------------------------------------------------------------------
# Add product
# ---------------------------------------------------------------------------

class TestAddProduct:
    def test_new_product_appears_in_table(self, page: Page, base_url: str):
        open_app(page, base_url)
        fill_add_form(page, id_=50, name="Yogurt", price=79.9)
        expect(page.get_by_test_id("cell-name-50")).to_be_visible()
        expect(page.get_by_test_id("cell-name-50")).to_have_text("Yogurt")

    def test_row_count_increases(self, page: Page, base_url: str):
        open_app(page, base_url)
        fill_add_form(page, id_=51, name="Butter", price=120.0)
        rows = page.get_by_test_id("products-body").locator("tr")
        expect(rows).to_have_count(3)

    def test_form_clears_after_submit(self, page: Page, base_url: str):
        open_app(page, base_url)
        fill_add_form(page, id_=52, name="Cream", price=55.0)
        expect(page.get_by_test_id("input-name")).to_have_value("")

    def test_duplicate_id_shows_error(self, page: Page, base_url: str):
        open_app(page, base_url)
        fill_add_form(page, id_=1, name="Duplicate", price=10.0)
        error = page.get_by_test_id("add-error")
        expect(error).to_be_visible()
        expect(error).not_to_be_empty()

    def test_duplicate_id_does_not_add_row(self, page: Page, base_url: str):
        open_app(page, base_url)
        fill_add_form(page, id_=1, name="Duplicate", price=10.0)
        rows = page.get_by_test_id("products-body").locator("tr")
        expect(rows).to_have_count(2)


# ---------------------------------------------------------------------------
# Edit product
# ---------------------------------------------------------------------------

class TestEditProduct:
    def test_click_edit_opens_modal(self, page: Page, base_url: str):
        open_app(page, base_url)
        page.get_by_test_id("btn-edit-1").click()
        expect(page.get_by_test_id("modal-overlay")).to_be_visible()

    def test_modal_prefilled_with_name(self, page: Page, base_url: str):
        open_app(page, base_url)
        page.get_by_test_id("btn-edit-1").click()
        expect(page.get_by_test_id("edit-name")).to_have_value("Milk")

    def test_modal_prefilled_with_price(self, page: Page, base_url: str):
        open_app(page, base_url)
        page.get_by_test_id("btn-edit-1").click()
        expect(page.get_by_test_id("edit-price")).to_have_value("89.90")

    def test_cancel_closes_modal(self, page: Page, base_url: str):
        open_app(page, base_url)
        page.get_by_test_id("btn-edit-1").click()
        page.get_by_test_id("btn-cancel").click()
        expect(page.get_by_test_id("modal-overlay")).to_be_hidden()

    def test_click_outside_closes_modal(self, page: Page, base_url: str):
        open_app(page, base_url)
        page.get_by_test_id("btn-edit-1").click()
        page.get_by_test_id("modal-overlay").click(position={"x": 5, "y": 5})
        expect(page.get_by_test_id("modal-overlay")).to_be_hidden()

    def test_save_updates_name_in_table(self, page: Page, base_url: str):
        open_app(page, base_url)
        page.get_by_test_id("btn-edit-1").click()
        page.get_by_test_id("edit-name").fill("Whole Milk")
        page.get_by_test_id("btn-save").click()
        expect(page.get_by_test_id("cell-name-1")).to_have_text("Whole Milk")

    def test_save_closes_modal(self, page: Page, base_url: str):
        open_app(page, base_url)
        page.get_by_test_id("btn-edit-1").click()
        page.get_by_test_id("edit-name").fill("Whole Milk")
        page.get_by_test_id("btn-save").click()
        expect(page.get_by_test_id("modal-overlay")).to_be_hidden()


# ---------------------------------------------------------------------------
# Delete product
# ---------------------------------------------------------------------------

class TestDeleteProduct:
    def test_row_disappears_after_delete(self, page: Page, base_url: str):
        open_app(page, base_url)
        page.get_by_test_id("btn-delete-1").click()
        expect(page.get_by_test_id("product-row-1")).not_to_be_visible()

    def test_row_count_decreases(self, page: Page, base_url: str):
        open_app(page, base_url)
        page.get_by_test_id("btn-delete-1").click()
        rows = page.get_by_test_id("products-body").locator("tr")
        expect(rows).to_have_count(1)

    def test_delete_all_shows_empty_message(self, page: Page, base_url: str):
        open_app(page, base_url)
        page.get_by_test_id("btn-delete-1").click()
        page.get_by_test_id("btn-delete-2").click()
        expect(page.get_by_test_id("empty-msg")).to_be_visible()
