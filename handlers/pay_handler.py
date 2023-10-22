from aiogram import Bot, Router, F
from aiogram.types import PreCheckoutQuery, Message

from utils.data import get_user_id, set_pay_order


dp = Router()

async def process_successful_payment(message: Message):
    successful_payment = message.successful_payment
    order_info = successful_payment.order_info
    total_amount = successful_payment.total_amount
    currency = successful_payment.currency

    # Вывод информации о заказе
    print("Информация о заказе:")
    print("Номер заказа:", order_info)
    print("Сумма заказа:", total_amount, currency)

@dp.pre_checkout_query()
async def process_precheck(precheck: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(precheck.id, ok=True)

@dp.message(F.successful_payment)
async def process_pay(message: Message):
    user_id = get_user_id(message.from_user.id)
    await set_pay_order(user_id)
    await process_successful_payment(message)