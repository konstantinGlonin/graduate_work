from tenacity import Retrying, stop_after_attempt, wait_exponential

from lib.config import Config

config = Config()
backoff = Retrying(stop=stop_after_attempt(config.elt.retry_attempt),
                   wait=wait_exponential(
                       multiplier=config.elt.wait_exp_mult,
                       min=config.elt.wait_exp_min,
                       max=config.elt.wait_exp_max))
