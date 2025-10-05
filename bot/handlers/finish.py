from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards.inline import finish_keyboard
from bot.utils.format import format_product
from bot.utils.api_client import create_product_from_bot_data, save_rating_from_bot, save_comment_from_bot

router = Router()


@router.callback_query(F.data == "finish")
async def handle_finish(callback: CallbackQuery, state: FSMContext):
    await finish(callback, state)


async def finish(message_or_callback, state: FSMContext):
    product_data = await state.get_data()
    
    try:
        # Create the product in the database
        api_response = await create_product_from_bot_data(product_data)
        product_id = api_response['id']
        
        # Save ratings
        if product_data.get('rating_arina'):
            await save_rating_from_bot(
                product_id, 
                product_data.get('telegram_id_arina'), 
                product_data['rating_arina']
            )
        
        if product_data.get('rating_andrew'):
            await save_rating_from_bot(
                product_id, 
                product_data.get('telegram_id_andrew'), 
                product_data['rating_andrew']
            )
        
        # Save comments
        if product_data.get('comment_arina'):
            await save_comment_from_bot(
                product_id, 
                product_data.get('telegram_id_arina'), 
                product_data['comment_arina']
            )
        
        if product_data.get('comment_andrew'):
            await save_comment_from_bot(
                product_id, 
                product_data.get('telegram_id_andrew'), 
                product_data['comment_andrew']
            )
        
        # Clear state and show formatted product
        await state.clear()
        
        text = format_product(product_data)
        message = message_or_callback.message or message_or_callback
        await message.answer(f"✅ Product saved successfully!\n\n{text}", reply_markup=finish_keyboard())
        
    except Exception as e:
        # If API call fails, still show the formatted product but with error message
        await state.clear()
        
        text = format_product(product_data)
        message = message_or_callback.message or message_or_callback
        await message.answer(f"⚠️ Product created locally (API error: {str(e)})\n\n{text}", reply_markup=finish_keyboard())

