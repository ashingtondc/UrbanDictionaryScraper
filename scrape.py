from scrape_utils import scrape_letter
import logging
import multiprocessing as mp

logging.basicConfig(
    filename='scrape.log', 
    filemode='a',
    level=logging.INFO, 
    format='%(asctime)s %(levelname)s %(message)s', 
    datefmt='%m/%d/%Y %I:%M:%S %p')

pool = mp.Pool(processes=4)
results = [pool.apply_async(scrape_letter, args=[i]) for i in range(65, 91)]
output = [p.get() for p in results]
pool.close()

# for i in range(65, 91):
#     scrape_letter(i)
