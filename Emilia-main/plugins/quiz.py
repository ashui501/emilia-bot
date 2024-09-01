import requests, asyncio, random,time
from threading import Timer
from pyrogram import Client, filters
from collections import Counter
from pyrogram.types import InlineKeyboardMarkup, CallbackQuery, InlineKeyboardButton

rounds = 0
user_id = 0
a = []
c_a = []


def fetch_trivia_questions(amount):
    url = f"https://opentdb.com/api.php?amount={amount}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        questions = []
        for result in data["results"]:
            question = result["question"]
            correct_answer = result["correct_answer"]
            incorrect_answers = result["incorrect_answers"]
            questions.append(
                {
                    "question": question,
                    "correct_answer": correct_answer,
                    "incorrect_answers": incorrect_answers,
                }
            )
        return questions
    else:
        print("Failed to fetch trivia questions")


def generate_quiz(correct_answer, incorrect_options, num_variables=4):
    options = [correct_answer] + incorrect_options
    random.shuffle(options)
    return options


@Client.on_message(filters.command("qiz"))
async def qz(client, message):
    keybord = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("5 Quizs", callback_data="q_5"),
                InlineKeyboardButton("10 Quizs", callback_data="q_10"),
                InlineKeyboardButton("13 Quizs", callback_data="q_13"),
            ]
        ]
    )
    global start_reply, user_id
    user_id = message.from_user.id
    start_reply = await client.send_video(
        message.chat.id,
        "Images/quiz.mp4",
        f"• 🎐 {message.from_user.username} you joined the Quiz the Game!\nChoose how many rounds of quiz you want play!",
        reply_markup=keybord,
    )


async def asked(client, chat_id, callback_query, question, options):
    global rounds
    rounds += 1
    c_a.append(questions[rounds]["correct_answer"])
    buttons = [
        [InlineKeyboardButton(text=f"{i}", callback_data=f"a_{i}")] for i in options
    ]
    keybord = InlineKeyboardMarkup(buttons)
    await client.edit_message_text(
        chat_id, start_reply.id, question, reply_markup=keybord
    )
    options = generate_quiz(
        questions[rounds]["correct_answer"], questions[rounds]["incorrect_answers"]
    )
    await countdown(client, callback_query, questions[rounds]["question"], options)


def timeout(client, callback_query, question, options):
    asyncio.run(
        asked(client, callback_query.message.chat.id, callback_query, question, options)
    )


async def countdown(client, callback_query, question, options):
    print("wait 5 sec")
    global t
    t = Timer(5.0, timeout, args=(client, callback_query, question, options))
    t.start()


def clear_all():
    global amount, user_id, rounds
    a.clear()
    c_a.clear()
    amount = 0
    user_id = 0
    rounds = 0


def score(list1, list2):
    # Create frequency counters for both lists
    counter_list1 = Counter(list1)
    counter_list2 = Counter(list2)

    # Find the difference between the two counters
    differences = counter_list1 - counter_list2

    # Calculate the total number of differences
    total_differences = sum(differences.values())

    return total_differences


@Client.on_callback_query(filters.regex("q_(.*)"))
async def switch(client, callback_query: CallbackQuery):
    global questions, amount
    amount = int(callback_query.data.split("_", 1)[1]) + 1
    questions = fetch_trivia_questions(amount)
    options = generate_quiz(
        questions[rounds]["correct_answer"], questions[rounds]["incorrect_answers"]
    )
    await asked(
        client,
        callback_query.message.chat.id,
        callback_query,
        questions[rounds]["question"],
        options,
    )


@Client.on_callback_query(filters.regex("a_(.*)"))
async def switch_2(client, callback_query: CallbackQuery):
    a.append(callback_query.data.split("_", 1)[1])
    try:
        if rounds < amount:
            if user_id == callback_query.from_user.id:
                options = generate_quiz(
                    questions[rounds]["correct_answer"],
                    questions[rounds]["incorrect_answers"],
                )
                t.cancel()
                await asked(
                    client,
                    callback_query.message.chat.id,
                    callback_query,
                    questions[rounds]["question"],
                    options,
                )
            else:
                await client.answer_callback_query(
                    callback_query_id=callback_query.id,
                    text="This is not your game!🎮\n Use /qiz to play!",
                    show_alert=True,
                )
        else:
            pass
    except:
        s = score(a, c_a)
        await client.edit_message_text(
            callback_query.message.chat.id,
            start_reply.id,
            f"• 🎐 your score is {amount - s} (This message will be delete with in 3 sec)",
        )
        clear_all()
        time.sleep(3)
        await callback_query.message.delete()
