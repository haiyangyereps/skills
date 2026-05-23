---
name: wechat-mac-client
description: Operate the user's logged-in personal WeChat Mac client through visible desktop UI. Use when the user asks to read visible WeChat messages, search a contact or group, draft a WeChat reply, or send a WeChat message with explicit confirmation. Do not use for database decryption, background monitoring, credential handling, bypassing login, or bulk unsolicited messaging.
---

# WeChat Mac Client

## Scope

Use only the logged-in WeChat Mac desktop client and only through visible UI automation.

Allowed:

- Read text that is visible in the active WeChat window.
- Search for a contact or group by user-provided name.
- Draft a message for a chosen recipient.
- Send a message only after the user explicitly confirms the recipient and full message.
- Scroll the current chat only when the user asks to inspect more history.

Not allowed:

- Decrypt or inspect WeChat local databases.
- Extract cookies, tokens, passwords, session files, or private keys.
- Bypass login, verification, device trust, payment confirmation, or access controls.
- Run hidden background monitoring.
- Send bulk unsolicited messages or spam.
- Read conversations unrelated to the user's current request.

## Preflight

1. Confirm the task type: read visible messages, draft a message, or send a confirmed message.
2. Use the Mac desktop UI. Prefer Computer Use for clicking, typing, screenshots, and reading visible UI.
3. If WeChat is not open, ask before launching it.
4. If WeChat requires login, password, QR scan, verification, or device confirmation, stop and ask the user to complete it.
5. If macOS blocks screen reading or UI control, tell the user which permission is needed.

## Reading Messages

1. Work only in the current chat unless the user names another contact or group.
2. If the target chat is not open, search for the exact user-provided contact or group name.
3. Read only visible message text and sender/time labels that are visible.
4. If the user asks for older messages, scroll the current chat incrementally and summarize what becomes visible.
5. Do not claim the full chat history was read unless the user provided an export or all relevant history was visibly inspected.

## Drafting Messages

1. Identify the intended recipient or group.
2. Compose the message in the user's requested tone and language.
3. If the user only asked to draft, do not place text in WeChat unless asked.
4. If placing text into the WeChat input box, do not send until confirmation.

## Sending Messages

Default behavior is confirmation-before-send.

Before pressing Enter or clicking Send, show:

- Recipient or group name.
- Full message content.
- A direct question asking whether to send now.

Proceed only if the user confirms in the current conversation. If the user already gave an exact recipient and exact message and explicitly said to send it, you may send without another confirmation unless the recipient match is ambiguous.

After sending, verify by reading the last visible outgoing message when possible.

## Ambiguity Handling

Stop and ask the user when:

- Multiple contacts or groups match the name.
- The active chat does not match the intended recipient.
- The message includes money, account credentials, legal commitments, medical advice, or other high-impact content.
- WeChat opens a confirmation dialog, payment flow, login prompt, or permission request.

## Output

When reading, summarize only the relevant visible messages.

When drafting, provide the draft text and state that it has not been sent.

When sending, state whether the message was sent and what visible evidence confirmed it.

