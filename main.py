import logging
from telegram import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from articulo import *
from conexiones import *

TOKEN = "AGREGA AQUÍ TU TOKEN"


users = {}

bot = Bot(TOKEN)

KB_UNIDADES = [
    [InlineKeyboardButton("Piezas", callback_data="pzs"),
        InlineKeyboardButton("Litros", callback_data="lts")],
    [InlineKeyboardButton("Kilosgramos", callback_data="kgs"),
        InlineKeyboardButton("Metros", callback_data="mts")],
]

KB_OPCION = [
    [InlineKeyboardButton("Eliminar lista", callback_data="si")],
]


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        """Hola {}!\n
Usa /help para saber que puedo hacer""".format(update.effective_user.username)
    )


def miembros(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        """
ouarit
        """
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        """Usa /start para recibir un saludo\n
Usa /registrar para agregar un producto\n
Usa /miembros para saber quienes estan destrás de este bot :D
Usa /lista para obtener tu lista de productos"""
    )


def inicializar_usuario(update, context):
    global users
    if update.effective_user.id not in users:
        users[update.effective_user.id] = articulo(False)


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    global users
    query = update.callback_query

    query.answer()

    if query.data == "si":
        eliminar_articulo(update.effective_user.id)
        query.edit_message_text(
            "Lista eliminada correctamente")
        return

    if users[update.effective_user.id].is_registro():

        users[update.effective_user.id].set_unidad(query.data)

        users[update.effective_user.id].finalizar_registro()

        # aqui se hace la alta en mongo

        insertar_datos(users[update.effective_user.id],
                       update.effective_user.id)

        users[update.effective_user.id] = None

        query.edit_message_text(
            "Producto registrado correctamente")

        return


def answer_command(update: Update, context: CallbackContext) -> None:
    global users

    if users[update.effective_user.id].is_registro():
        registro(update, context)
        return


def registro(update, context) -> None:
    global users

    if users[update.effective_user.id].is_nombre_empty():
        users[update.effective_user.id].set_nombre(update.message.text)

        update.message.reply_text(
            "Ingresa la cantidad"
        )

        return

    if users[update.effective_user.id].is_cantidad_empty():

        users[update.effective_user.id].set_cantidad(update.message.text)

        reply_markup = InlineKeyboardMarkup(KB_UNIDADES)

        update.message.reply_text(
            "Ingresa la unidad de medida", reply_markup=reply_markup
        )
        return


def registrar(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    global users
    inicializar_usuario(update, context)

    users[update.effective_user.id] = articulo(True)

    update.message.reply_text(
        "Ingresa el nombre del producto"
    )


def obtener_lista(update: Update, context: CallbackContext) -> None:

    global users

    inicializar_usuario(update, context)

    if contador_articulos(update.effective_user.id) == 0:
        update.message.reply_text(
            "No tienes productos registrados"
        )
        return

    global users
    text = ""

    for articulo in get_lista(update.effective_user.id):
        text = text + "Nombre: {}\nCantidad: {} {}".format(
            articulo["nombre"], articulo["cantidad"], articulo["unidad"])

    reply_markup = InlineKeyboardMarkup(KB_OPCION)
    update.message.reply_text(
        text=text, reply_markup=reply_markup
    )

    return


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("miembros", miembros))
    dispatcher.add_handler(CommandHandler(
        "registrar", registrar))
    dispatcher.add_handler(CommandHandler(
        "lista", obtener_lista))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, answer_command))

    # on button click
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
