import asyncio, datetime
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome')
        ctx = await b.new_context(viewport={'width': 390, 'height': 760}, device_scale_factor=3, is_mobile=True, has_touch=True)
        pg = await ctx.new_page()
        for nome, url in [('resenhas', 'https://eliteboardgamers.com.br/resenhas/')]:
            await pg.goto(url, wait_until='networkidle'); await pg.wait_for_timeout(1500)
            await pg.screenshot(path=f'prints/{nome}.png')
        print('capturado', datetime.datetime.now().isoformat())
        await b.close()
asyncio.run(main())
