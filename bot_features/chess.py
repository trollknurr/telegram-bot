import re
import os
import subprocess

import telegram
import chess

from tinydb import TinyDB

from .fen2png.fen2png import chess_position_img


game_id_re = re.compile(r'/reg_second_chess_player (?P<game_id>\d+)', flags=re.IGNORECASE)
board_re = re.compile(r'/get_board (?P<game_id>\d+)', flags=re.IGNORECASE)
turn_re = re.compile(r'^/make_turn (?P<game_id>\d+) (?P<turn>\w+)$', flags=re.IGNORECASE)

CHESS_FIGURES = dict(zip("KQRBNPkqrbnp", "♔♕♖♗♘♙♚♛♜♝♞♟"))
DESTINATION = os.environ['REMOTE_IMG_SSH']
URL_DESTINATION = os.environ['DESTINATION_URL']
db = TinyDB('chess.json')
chess_db = db.table('chess')


def start_new_game(bot, update):
    board = chess.Board()
    game_id = chess_db.insert({
        'player_to_move': update.message.from_user.id,
        'player_has_moved': None,
        'board': board.fen()
    })

    bot.sendMessage(update.message.chat_id,
                    text="Зарегестрируйте своего оппонента командой */reg_second_chess_player {}*".format(game_id),
                    parse_mode=telegram.ParseMode.MARKDOWN
                    )


def register_second_player(bot, update):
    try:
        game_id = int(game_id_re.match(update.message.text).groupdict()['game_id'])
    except KeyError:
        bot.sendMessage(update.message.chat_id, text="Не предоставлен идентификатор партии!")
        return

    chess_db.update({
        'player_has_moved': update.message.from_user.id
    }, eids=(game_id,))
    game_data = chess_db.get(eid=game_id)
    bot.sendMessage(game_data['player_to_move'], text="Игра инициализированна, можно делать ход")
    bot.sendMessage(update.message.chat_id, text="Вы подключены к игре!")


def make_turn(bot, update):
    turn_data = turn_re.match(update.message.text).groupdict()
    try:
        game_id = int(turn_data['game_id'])
        turn = turn_data['turn']
    except KeyError:
        bot.sendMessage(update.message.chat_id, text="Не предоставлен идентификатор партии или ход!")
        return
    game_data = chess_db.get(eid=game_id)
    if game_data['player_to_move'] != update.message.from_user.id:
        bot.sendMessage(update.message.chat_id, text="Сейчас ходит сопреник!")
        return

    board = chess.Board(fen=game_data['board'])
    try:
        board.push_san(turn)
    except ValueError:
        bot.sendMessage(update.message.chat_id, text="Так ходить нельзя!")
        return

    if board.is_game_over():
        for user_id in (game_data['player_to_move'], game_data['player_has_moved']):
            bot.sendMessage(user_id, text="Игра окончена")
    else:
        chess_db.update({
            'player_to_move': game_data['player_has_moved'],
            'player_has_moved': game_data['player_to_move'],
            'board': board.fen()
        }, eids=(game_id,))
        updated_game_data = chess_db.get(eid=game_id)
        bot.sendMessage(updated_game_data['player_to_move'],
                        text="Ваш ход ( /make_turn {} )".format(game_id))
        # отправить картинку доски
        board_img = chess_position_img(board.board_fen())
        file_name = '{}.png'.format(game_id)
        p = '/tmp/' + file_name
        board_img.save(p, 'PNG')
        p = subprocess.Popen(["scp", p, DESTINATION.format(file_name)])
        os.waitpid(p.pid, 0)
        bot.sendPhoto(chat_id=updated_game_data['player_to_move'],
                      photo=URL_DESTINATION.format(file_name))

        bot.sendMessage(update.message.chat_id, text="Ваш ход принят")


def get_board(bot, update):
    try:
        game_id = int(board_re.match(update.message.text).groupdict()['game_id'])
    except KeyError:
        bot.sendMessage(update.message.chat_id, text="Не предоставлен идентификатор партии!")
        return
    game_data = chess_db.get(eid=game_id)
    board = chess.Board(fen=game_data['board'])
    board_img = chess_position_img(board.board_fen())
    file_name = '{}.png'.format(game_id)
    p = '/tmp/' + file_name
    board_img.save(p, 'PNG')
    p = subprocess.Popen(["scp", p, DESTINATION.format(file_name)])
    os.waitpid(p.pid, 0)
    bot.sendPhoto(chat_id=update.message.chat_id,
                  photo=URL_DESTINATION.format(file_name))


def register_bot_feature(dispatcher):
    dispatcher.addTelegramCommandHandler("chess", start_new_game)
    dispatcher.addTelegramCommandHandler("reg_second_chess_player", register_second_player)
    dispatcher.addTelegramCommandHandler("make_turn", make_turn)
    dispatcher.addTelegramCommandHandler("get_board", get_board)
    # Закрываем базу при выключении
    return db.close
