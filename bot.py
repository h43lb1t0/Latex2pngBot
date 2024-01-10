import io
import os
import re
import subprocess
import interactions
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')

bot = interactions.Client(token=discord_token)

def convertLatex2Png(latex: str) -> tuple[str | io.BytesIO, bool]:
    latex_pattern = re.compile(
        r'\\(?:begin|end){(?:equation|align|gather|multline)\*?}|'
        r'\\\[.*?\\\]|'
        r'\$.*?\$|'
        r'\\frac{.*?}{.*?}|'
        r'\\sqrt{.*?}|'
        r'\\text{.*?}|'
        r'\\[a-zA-Z]+'
    )
    import matplotlib.pyplot as plt

    latex = rf"${latex}$"

    try:

        fig = plt.figure(figsize=(3, 0.5))  # Dimensions of figsize are in inches
        text = fig.text(
            x=0.5,  # x-coordinate to place the text
            y=0.5,  # y-coordinate to place the text
            s=latex,
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=16,
        )

        buffer = io.BytesIO()

        fig.savefig(buffer, dpi=500, transparent=False, bbox_inches="tight", pad_inches=0.05, format="png")

    except Exception as e:
        return f"Error: {e}", False

    buffer.seek(0)
    return buffer, True
    
    
@interactions.slash_command(name='latex2png', description='Convert LaTeX to PNG')
@interactions.slash_option(
    name="latex",
    description="The latex formula",
    required=True,
    opt_type=interactions.OptionType.STRING
)
async def latex2png(ctx, latex: str):
    latex, success = convertLatex2Png(latex)
    if success:
        await ctx.send(file=interactions.File(file=latex, content_type="image", file_name="formula.png"))
    else:
        await ctx.send(latex)

bot.start()