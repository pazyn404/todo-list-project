from math import ceil


def get_page_number_after_deletion(page, count, per_page) -> int:
    per_page = max(per_page, 1)

    count -= 1
    if ceil(count / per_page) < page:
        page = max(page - 1, 1)

    return page
