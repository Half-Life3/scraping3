from venv import logger

from prefect import flow, tasks, task

from main import scrape_item_prices


@task(retries=2)
def scraping():
    logger.info('scraping......')


@flow
def main_flow(urls: list[str] = None):
    if urls is None:
        return 'URL IS NOT EXIST'
    for url in urls:
        scrape_item_prices(url)


if __name__ == "__main__":
    main_flow.serve(
        name='scraping-deployment',
        cron='*/2 * * * *',
        parameters={'urls': ['https://coinmarketcap.com/currencies/bitcoin/']},
        tags=['production'],
        description='Scraping Prefect Flow'
    )
