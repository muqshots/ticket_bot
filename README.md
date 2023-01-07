# ticket_bot
You can find an example [here](https://github.com/jvherck/ticket_bot/blob/master/src/ansi_example.py).

## IMPORTANT
I suggest you use `io.BytesIO(Transcript.encoded)` like in the example, if you're sending it as a `discord.File`. \
This encoding (`cp1252`) allows special ANSI characters to exist and won't turn them into weird characters, so it doesn't f*ck up your html transcript. \
You can still just get the standard html string by using `Transcript.html`.
