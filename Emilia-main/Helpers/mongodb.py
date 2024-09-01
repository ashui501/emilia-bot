from datetime import datetime
import pymongo
from pymongo import ReturnDocument

client = pymongo.MongoClient(
    "mongodb+srv://debayankun:das1234@cluster0.jeihm5r.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
mongo = client["DataBase"]
userscol = mongo["users"]
chatscol = mongo["chats"]


def fetch(id, card_id):
    document = userscol.find_one({"user_id": 214212415})
    first_card = document["cards"][card_id]
    image = first_card["image"]
    description = first_card["des"]
    card_name = first_card["name"]
    print(f"Image: {image}")
    print(f"Description: {description}")
    print(f"Card Name: {card_name}")


def add_user(
    name,
    user_id,
    ban=False,
    date=datetime.now().strftime("%Y-%m-%d"),
    cards=None,
    deck=None,
):
    user = userscol.find_one({"user_id": user_id})
    if user is None:
        new_user = {
            "name": name,
            "user_id": user_id,
            "banned": ban,
            "joined": date,
            "cards": cards,
        }
        userscol.insert_one(new_user)
        print(f"User {name} added to the collection.")
    else:
        print(f"User with user_id {user_id} already exists in the collection.")


#
# cards = [
#    {"id": "1", "image": "image1.png", "des": "First card description", "name": "Card1"},
#    {"id": "2", "image": "image2.png", "des": "Second card description", "name": "Card2"}
# ]
# add_user("Alice", "12345", False, datetime.now(), True, True,cards)


def check_deck(user_id):
    document = userscol.find_one({"user_id": user_id})

    if not document:
        raise ValueError("Document with the provided ID does not exist.")

    deck = document.get("deck", [])

    if not isinstance(deck, list):
        raise ValueError("'deck' field is not an array.")

    if len(deck) == 10:
        return False
    return True


def push_cards(user_id, card):
    user = userscol.find_one({"user_id": user_id})
    print(user["cards"])
    if check_deck(user_id):
        if user["deck"] is None:
            userscol.update_one({"user_id": user_id}, {"$set": {"deck": [card]}})
        else:
            userscol.update_one({"user_id": user_id}, {"$push": {"deck": card}})
    else:
        if user["cards"] is None:
            userscol.update_one({"user_id": user_id}, {"$set": {"cards": [card]}})
        else:
            userscol.update_one({"user_id": user_id}, {"$push": {"cards": card}})


def move_deck(user_id, element_id):

    # Find the document by its ID and the element in the deck
    document = userscol.find_one({"user_id": user_id})

    if not document:
        raise ValueError("Document with the provided ID does not exist.")

    deck = document.get("deck", [])

    if element_id not in deck:
        raise ValueError(f"Element with ID {element_id} not found in deck.")

    # Perform the update: remove the element from deck and add it to cards
    updated_document = userscol.find_one_and_update(
        {"user_id": user_id},
        {
            "$pull": {"deck": element_id},  # Remove from deck
            "$push": {"cards": element_id},  # Add to cards
        },
        return_document=ReturnDocument.AFTER,  # Return the updated document
    )

    return updated_document


def move_cards(user_id, element_id):

    # Find the document by its ID and the element in the cards array
    document = userscol.find_one({"user_id": user_id})

    if not document:
        raise ValueError("Document with the provided ID does not exist.")

    cards = document.get("cards", [])

    if element_id not in cards:
        raise ValueError(f"Element with ID {element_id} not found in cards.")

    # Perform the update: remove the element from cards and add it to deck
    updated_document = userscol.find_one_and_update(
        {"user_id": user_id},
        {
            "$pull": {"cards": element_id},  # Remove from cards
            "$push": {"deck": element_id},  # Add to deck
        },
        return_document=ReturnDocument.AFTER,  # Return the updated document
    )

    return updated_document


# card = {"id": "3", "image": "image1.png", "des": "First card description", "name": "Card3"}
# push_cards("12345",card)


def add_chats(
    chat_id,
    date=datetime.now().strftime("%Y-%m-%d"),
    ban=None,
    captcha=False,
    event=False,
):
    chat = chatscol.find_one({"chat_id": chat_id})
    if chat is None:
        new_user = {
            "chat_id": chat_id,
            "banned": ban,
            "joined": date,
            "captcha": captcha,
            "event": event,
        }
        chatscol.insert_one(new_user)
        print(f"chat_name added to the collection.")
    else:
        print(f"chat_name with chat_id {chat_id} already exists in the collection.")


def ban(chat_id, users):
    chat = chatscol.find_one({"chat_id": chat_id})
    print(chat["banned"])
    if chat is None:
        add_chats(chat_id=chat_id)
        if chat["banned"] is None:
            chatscol.update_one({"chat_id": chat_id}, {"$set": {"banned": [users]}})
        else:
            chatscol.update_one({"chat_id": chat_id}, {"$push": {"banned": users}})
    else:
        if chat["banned"] is None:
            chatscol.update_one({"chat_id": chat_id}, {"$set": {"banned": [users]}})
        else:
            chatscol.update_one({"chat_id": chat_id}, {"$push": {"banned": users}})


# user = {"user_id": "4", "date": datetime.now().strftime("%Y-%m-%d"), "reason": "fun"}
# add_chats("Das fads",4152428714545)
# ban(41524214545,user)


def unban(chat_id, user_id):
    try:
        result = chatscol.update_one(
            {"chat_id": chat_id}, {"$pull": {"banned": {"user_id": user_id}}}
        )
        if result.modified_count > 0:
            return f"{user_id} removed from the 'banned' list {chat_id}."
        else:
            return f"User not found!"
    except:
        return


# unban(41524214545,"3")


def captcha(chat_id, captcha):
    chat = userscol.find_one({"chat_id": chat_id})
    if chat is None:
        add_chats(chat_id=chat_id, captcha=captcha)
    else:
        chatscol.update_one({"chat_id": chat_id}, {"$set": {"captcha": captcha}})


def event(chat_id, event):
    chat = userscol.find_one({"chat_id": chat_id})
    if chat is None:
        add_chats(chat_id=chat_id, event=event)
    else:
        chatscol.update_one({"chat_id": chat_id}, {"$set": {"event": event}})


def give(source_user_id, target_user_id, card_id):

    # Find the card in the source user's array
    source_user = userscol.find_one(
        {"user_id": source_user_id, "cards.id": card_id}, {"cards.$": 1}
    )

    if not source_user or "cards" not in source_user:
        print(
            f"Card with ID {card_id} not found in source user ID {source_user_id}'s cards."
        )
        return

    # Extract the card to be moved
    card_to_move = source_user["cards"][0]

    # Pull the card from the source user's array
    pull_result = userscol.update_one(
        {"user_id": source_user_id}, {"$pull": {"cards": {"id": card_id}}}
    )

    if pull_result.modified_count == 0:
        print(
            f"Failed to remove card with ID {card_id} from source user ID {source_user_id}'s cards."
        )
        return

    # Push the card to the target user's array
    push_result = userscol.update_one(
        {"user_id": target_user_id}, {"$push": {"cards": card_to_move}}
    )

    if push_result.modified_count > 0:
        print(
            f"Card with ID {card_id} moved from user ID {source_user_id} to user ID {target_user_id}."
        )
    else:
        print(
            f"Failed to add card with ID {card_id} to target user ID {target_user_id}'s cards."
        )
        # If the push fails, you may want to add the card back to the source user's cards array
        userscol.update_one(
            {"user_id": source_user_id}, {"$push": {"cards": card_to_move}}
        )
        print(
            f"Card with ID {card_id} returned to source user ID {source_user_id}'s cards due to push failure."
        )


#give("12345", 214212415, "2")
