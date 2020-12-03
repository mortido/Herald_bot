from typing import List
from ai.chart import Player, Game


def format_topic(topic):
    first_link = None
    ts = 0
    for message in topic.messages.values():
        if first_link is None or ts > message.pub_timestamp:
            ts = message.pub_timestamp
            first_link = message.link
    return f"- [{topic.title}]({first_link}) ({len(topic.messages)})"


def format_category(category, topics):
    return f'**{category}:**\n' + \
           '\n'.join(format_topic(topic) for topic in topics if topic.category == category)


def trim_len(string, max_len):
    return string if len(string) <= max_len else string[:max_len - 1] + "…"


def format_toop(chart_name, players: List[Player]):
    rows = ["```"]
    rows.append(chart_name.upper())
    rows.append("")
    rows.append("    PLAYER          LANGUAGE  W.R. SCORE")
    rows.append("----------------------------------------")
    for i, player in enumerate(players):
        rows.append("{}{}{}{}{}".format(
            str(i + 1).ljust(4),
            trim_len(player.username, 16).ljust(16),
            player.language.ljust(9),
            player.winrate.rjust(5),
            player.score.rjust(6)
        ))
    rows.append("```")
    return "\n".join(rows)


def format_top(chart_name, players: List[Player]):
    rows = ["```"]
    rows.append(chart_name.upper())
    rows.append("")
    rows.append("    PLAYER     SCORE")
    rows.append("--------------------")
    for i, player in enumerate(players):
        rows.append("{}{}{}".format(
            str(i + 1).ljust(4),
            trim_len(player.username, 11).ljust(11),
            player.score.rjust(5)
        ))
    rows.append("```")
    return "\n".join(rows)


def format_poos(chart_name, players):
    rows = ["```"]
    for i, player in players:
        rows.append("{}{}{}{}{}".format(
            str(i + 1).ljust(4),
            trim_len(player.username, 16).ljust(16),
            player.language.ljust(9),
            player.winrate.rjust(5),
            player.score.rjust(6)
        ))
    rows.append("```")
    return "\n".join(rows)


def format_pos(chart_name, players):
    rows = ["```"]
    for i, player in players:
        rows.append("{}{}{}".format(
            str(i + 1).ljust(4),
            trim_len(player.username, 11).ljust(11),
            player.score.rjust(5)
        ))
    rows.append("```")
    return "\n".join(rows)


import random

win_phrases = [
    "Ты на правильном пути",
    "Ты идешь хорошо",
    "Это реальный прогрес",
    "Ты хорошо поработал",
    "Улыбнись!",
    "Вот это да!",
    "Нифига себе!",
    "🔥🔥🔥",
    "Так держать!",
    "Продолжай в том же духе!",
    "mortido может лучше",
    "Не зазнавайся",
    "Ты можешь еще лучше!",
    "Как ты хорош!",
    "Как сильны твои лапищи!",
    "Ты на правильном пути",
    "Бах! Тыщ! Бум!",
    "Кажется, ты идёшь к победе!",
    "У тебя здорово получается!",
    "Чем выше поднимаешься - тем больнее падать.",
    "Интересно, это заслуженная победа, или просто повезло?",
    "Уверенно.",
    "Like a boss.",
    "Держи `1u + pos.x + width_ * (1u + pos.y)` - это кусок кода mortido, он приносит segfault'ы",
]

loose_phrases = [
    "Бывает и хуже",
    "Слезами горю не поможешь",
    "На этой игре свет клином не сошелся",
    "Зато ты веселый",
    "Твоя мама тебя любит",
    "Противнику просто повезло",
    "Ты проиграл битву, но не проиграл войну",
    "Это не конец света",
    "Commandos тоже терпел поражения",
    "Нет худа без добра",
    "Не сдавайся!",
    "Давай, ты можешь!",
    "Выше голову!",
    "Не вешай нос!",
    "Не унывай!",
    "Не... ну это совсем хреновая игра...",
    "Мы его запомним и отомстим",
    "Пожалуйста... Ну и не нужно...",
    "Держи `for (auto &entity : workers){` - это кусок кода Commandos'a, он приносит удачу",
    "У всех бывают осечки.",
    "Хорошо, когда есть, к чему стремиться.",
    "Каждое поражение делает тебя сильнее.",
    "Кажется, нужна ещё пара ифов...",
    "Хм... посмотришь, почему так вышло?",
    "Попробуй сменить язык",
]


def format_game(game: Game, player_idx):
    win = int(game.deltas[player_idx]) > 0
    rows = [random.choice(win_phrases if win else loose_phrases),
            f"http://russianaicup.ru/game/view/{game.gid}",
            "```",
            f"{game.gtype.ljust(10)}     SCORE    Δ   LB"]
    for i in range(len(game.scores)):
        player_prefix = "* " if i == player_idx else ""
        rows.append("{}{}{}{}{}".format(
            game.places[i].ljust(3),
            trim_len(player_prefix + game.players[i], 11).ljust(11),
            game.scores[i].rjust(6),
            game.deltas[i].rjust(5),
            game.global_places[i].rjust(5)
        ))
    rows.append("```")
    return "\n".join(rows)
