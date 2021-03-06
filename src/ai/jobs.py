from telegram.error import TelegramError
from telegram.ext import CallbackContext
from telegram import ParseMode

from subscriber import SubscriptionType
from ai import formatter
import logging
import time

logger = logging.getLogger(__name__)


def notify_about_new_games(context: CallbackContext):
    chart = context.job.context
    new_games = chart.get_new_games()
    if new_games:
        new_games.reverse()
        subs = context.bot.subscriber.get_subs_by_type(SubscriptionType.AI_GAMES)
        try:
            for sub in subs:
                for game in new_games:
                    post_it = False
                    player_idx = -1
                    for i, player in enumerate(game.players):
                        if player in sub.data:
                            post_it = True
                            player_idx = i
                            game.players[i] = player
                    if post_it:
                        context.bot.send_message(chat_id=sub.chat_id,
                                                 text=formatter.format_game(game, player_idx),
                                                 disable_web_page_preview=True,
                                                 parse_mode=ParseMode.MARKDOWN)
                        time.sleep(1/10)
        except BaseException as e:
            logger.error(f"Error during sending ai games: {e}")
        chart.reset_to_game(new_games[-1].gid)
