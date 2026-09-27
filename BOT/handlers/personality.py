import json

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from BOT.states.personality import PersonalityState

from BOT.keyboards.main import (
    personality_options_keyboard,
    personality_finish_keyboard,
)

from data.personality.questions import QUESTIONS

from core.personality.engine import PersonalityEngine

from core.personality.results import generate_result

from database.database import (
    save_personality_result,
)


router = Router()

engine = PersonalityEngine(QUESTIONS)


async def send_question(
    callback: CallbackQuery,
    state: FSMContext,
):

    data = await state.get_data()

    question_index = data.get(
        "question_index",
        0,
    )

    if question_index >= len(QUESTIONS):

        answers = data.get(
            "answers",
            {},
        )

        result = engine.calculate(
            answers
        )

        result_json = json.dumps(
            result,
            ensure_ascii=False,
        )

        save_personality_result(
            telegram_id=callback.from_user.id,
            result_json=result_json,
        )

        result_text = generate_result(
            result
        )

        await state.clear()

        await callback.message.edit_text(
            result_text,
            reply_markup=personality_finish_keyboard(),
        )

        return

    question = QUESTIONS[
        question_index
    ]

    progress = (
        f"🧠 سؤال "
        f"{question_index + 1}"
        f" از "
        f"{len(QUESTIONS)}"
    )

    text = (
        f"<b>{progress}</b>\n\n"
        f"{question['text']}"
    )

    await callback.message.edit_text(
        text,
        reply_markup=personality_options_keyboard(
            question
        ),
    )


@router.callback_query(
    F.data == "personality:start"
)
async def personality_start(
    callback: CallbackQuery,
    state: FSMContext,
):

    await callback.answer()

    await state.set_state(
        PersonalityState.answering
    )

    await state.update_data(
        question_index=0,
        answers={},
    )

    await send_question(
        callback,
        state,
    )


@router.callback_query(
    PersonalityState.answering,
    F.data.startswith(
        "personality:answer:"
    ),
)
async def personality_answer(
    callback: CallbackQuery,
    state: FSMContext,
):

    await callback.answer()

    try:
        option_index = int(
            callback.data.split(":")[-1]
        )

    except (
        ValueError,
        AttributeError,
    ):
        return

    data = await state.get_data()

    question_index = data.get(
        "question_index",
        0,
    )

    answers = data.get(
        "answers",
        {},
    )

    if question_index >= len(
        QUESTIONS
    ):
        return

    question = QUESTIONS[
        question_index
    ]

    if (
        option_index < 0
        or option_index >= len(
            question["options"]
        )
    ):
        return

    answers[
        str(question["id"])
    ] = option_index

    await state.update_data(
        answers=answers,
        question_index=question_index + 1,
    )

    await send_question(
        callback,
        state,
    )