# #!/usr/bin/env python3
# import os
# import argparse
import requests
# import sys

# def norm(phone: str) -> str:
#     digits = "".join(ch for ch in phone if ch.isdigit())
#     if not digits:
#         raise ValueError("phone contains no digits")
#     return f"{digits}@c.us"

# def main():
#     p = argparse.ArgumentParser(description="Send a simple WhatsApp text via open-wa EASY API")
#     p.add_argument("phone", help="Target phone (e.g. +1234567890)")
#     p.add_argument("message", help="Message text (wrap in quotes)")
#     p.add_argument("--api", help="EASY API base URL (default from OPENWA_API or http://localhost:8080)", default=None)
#     args = p.parse_args()

#     base = args.api or os.environ.get("OPENWA_API", "http://localhost:8080")
#     base = base.rstrip("/")

#     try:
#         chat = norm(args.phone)
#     except ValueError as e:
#         print("Bad phone:", e, file=sys.stderr)
#         sys.exit(2)

#     try:
#         resp = requests.post(f"{base}/sendText", json={"chatId": chat, "text": args.message}, timeout=10)
#         resp.raise_for_status()
#         print("Sent:", resp.text)
#     except Exception as e:
#         print("Failed to send message:", e, file=sys.stderr)
#         sys.exit(1)

# if __name__ == "__main__":
#     main()


# import requests

# BASE = "http://localhost:8080"  # your EASY API URL

# # If the endpoint needs any payload, put it here; otherwise send an empty dict
# payload = {}

# r = requests.post(f"{BASE}/getWAVersion", json=payload)




import json

def wa_request(api_url, method_or_endpoint, args=None, timeout=10):
    """
    Call any open-wa REST API method or endpoint.

    :param api_url: Base URL of wa-automate REST API, e.g., "http://localhost:8080"
    :param method_or_endpoint: Either a restricted method name (sendText, createGroup, etc.)
                               or a direct endpoint like "getAllChats"
    :param args: dict of arguments for the method/endpoint
    :param timeout: request timeout
    :return: JSON response if available, else raw text
    """
    args = args or {}

    # Decide if it's a restricted method (needs {"method":..., "args":...})
    restricted_methods = {"sendText", "createGroup", "getAllMessagesInChat", "videoCall", "call"}
    
    # if method_or_endpoint in restricted_methods:
    payload = {"method": method_or_endpoint, "args": args}
    url = api_url  # restricted methods use root endpoint
    # else:
    #     payload = args
    #     url = f"{api_url}/{method_or_endpoint}"  # direct endpoints
    
    r = requests.post(url, json=payload, timeout=timeout)
    print("status:", r.status_code)

    try:
        data = r.json()
        print("body:", json.dumps(data, indent=4, ensure_ascii=False))
        return data
    except json.JSONDecodeError:
        print("body is not valid JSON:", r.text)
        return r.text


# --- Examples of usage ---

wa_api = "http://localhost:8080"

# wa_request(wa_api, "sendText", {"to":"972532237008@c.us","content":"bannana"})



mavdak_date = "DATE"
participants = [ "972532237008" ]

s = f"""
מועמדים יקרים,
אנחנו מדור קצונה של אגף התקשוב. 
המיון לקצונה ייערך באופן מקוון ויכלול מבחנים ממוחשבים וראיון זום עם פסיכולוג. 

*המיון והראיונות לא מתקיימים באותו היום. המיון יהיה ב{mavdak_date} עבור כולם, ובהמשך נעדכן תאריכי ראיונות בקבוצה.*

לקראת המבדק שמתקיים ב{mavdak_date}, הכנו כמה דגשים חשובים, יש לקרוא את כלל ההוראות באופן יסודי!

✅הכנות למבדק : 
•יש לוודא כי יש לכם מחשב עם מצלמה לביצוע המבחנים 
•אין אפשרות לבצע את המבחנים עם מחשב של אפל , התוכנה של המבחנים לא נפתחת במחשב הזה
•אין אפשרות לבצע את המבחנים ללא מצלמה
•המבדק הוא חובה , אין אפשרות להזיז תאריך ונדרש לעלות בזמן לביצוע המבחנים
•במהלך השבוע שלאחר המבדק ישלחו אליכם פרטים על מועד ראיון הפסיכולוג - פרטי התחברות לזום (אין קישור- יש קוד), תאריך , שעה וסיסמה
•את המבחנים ואת הראיון יש לערוך בחדר שקט ללא הפרעות חיצוניות. 

• *אם מישהו לא מעוניין לצאת לקצונה/לדחות מחזור - להודיע בהקדם האפשרי!*

✅יום המבחנים :
•ביום המבחנים , יישלח לכם מייל עם קישור למבחנים עצמם לקראת השעה 9:00
•בשעה 9:00 יתקיים תדריך בזום לקראת המבחנים עצמם שאת הקישור אליו תקבלו כאן בקבוצה, לאחר סיום התדריך יש להיכנס לקישור של המבחן האישי ולהתחיל אותו
•אם יש לכם תקלה בזמן המבחנים , תכתבו בקבוצה מה התקלה עם צילום של המסך מחשב 
•בתמונת הקבוצה יש תקלות נפוצות , לפני שאתם כותבים בקבוצה על תקלה - תסתכלו אם יש את הפיתרון שלה בתמונה
•אורך המבחנים הינו 4-5 שעות בממוצע ולכן יש לפנות את הזמן בהתאם לכך. 
•יש לעלות למבחנים על מדים


✅יום ראיון הפסיכולוג :
•אין לבצע את הראיון משטח פתוח , פוסלים על זה ראיון
• יש לוודא שאתם נמצאים בחדר שקט ללא רעשים ושיש לכם קליטה
•יש להכיר את מה שנכתב עליכם בחוו״ד 870 שכתב עליכם המפקד הישיר
•במידה ועליתם לראיון והשיחה עוד לא התחילה , תכתבו בקבוצה כדי שנברר מול מדור מבדק
•זמן הריאיון הוא בערך בין רבע שעה לעשרים דקות , משתנה בין חייל לחייל.
•יש לעלות לראיון על מדים
•ניתן להתחבר לראיון מאפליקציית זום בטלפון ויש להוריד את האפליקציה מראש למכשיר 
•בתחילת הראיון תדרשו להציג חוגר ולענות על כמה שאלות אימות
"""

# Create group
group_resp = wa_request(
    wa_api,
    "createGroup",
    {
        "groupName": f"מבדק {mavdak_date}",
        "contacts": [p + "@c.us" for p in participants]
    }
)

gid = group_resp.get("gid") or group_resp.get("groupId") or group_resp.get("response", {}).get("_serialized")
if not gid:
    raise RuntimeError(f"Could not find group ID in response: {json.dumps(group_resp, indent=4, ensure_ascii=False)}")

# Send a message to the new group
wa_request(
    wa_api,
    "sendText",
    {"to": gid, "content": s}
)


# 2️⃣ Get all members actually in the group
members_resp = wa_request(
    wa_api,
    "getGroupMembersId",
    {"groupId": gid}
)
actual_members = set(members_resp)  # list of contactIds


# # 3️⃣ Compute participants who failed to be added
# failed_to_add = [p for p in participants if (p + "@c.us") not in actual_members]

# if failed_to_add:
#     # 4️⃣ Get group invite link
#     invite_info = wa_request(
#         wa_api,
#         "getGroupInviteLink",
#         {"groupId": gid}
#     )
#     invite_link = invite_info.get("link")
    
#     # 5️⃣ Send invite message to those who failed
#     invite_msg = f"Hi! You couldn't be added directly to the group. Join using this link: {invite_link}"
#     for p in failed_to_add:
#         wa_request(
#             wa_api,
#             "sendText",
#             {"to": p + "@c.us", "content": invite_msg}
#         )
