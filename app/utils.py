def notify(emoji, msg=None):
    emoji_map = {
        'disk': '\U0001f4be',
        'wrench': '\U0001f527',
        'gear': '\u2699\uFE0F',
        'success': '\u2728',
        'shake': '\U0001f91d',
        'praise': '\U0001f64c'
    }
    e = emoji_map[emoji]
    print(f'\n{e}   {msg}\n' if msg else f'\n\n\n {e}{e}{e} COMPLETE! {e}{e}{e} \n\n\n')