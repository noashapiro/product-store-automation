def setup_alert_handler(page, expected_message=None, count_alert=False):
    alert_message = ""
    alert_count = 0

    def handle_dialog(dialog):
        nonlocal alert_message, alert_count
        alert_message = dialog.message
        if count_alert:
            alert_count += 1
        assert dialog.type == "alert", f"Unexpected dialog type: {dialog.type}"
        if expected_message:
            assert expected_message in dialog.message, f"Unexpected alert message: {dialog.message}"
        dialog.accept()

    page.on("dialog", handle_dialog)
    return alert_message, alert_count


def home_page_displayed(setup_ui):
    home_page = setup_ui
    assert home_page.is_page_loaded(), "Home page did not load properly"
    return home_page

def get_product_by_inex(home_page,index):
    home_page.click_product(index)