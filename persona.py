from PIL import Image, ImageDraw, ImageFont

def save_persona_as_image(info, filename="persona_landscape.png"):
    width, height = 1400, 800
    margin = 50
    spacing = 40

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arialbd.ttf", 36)
        section_font = ImageFont.truetype("arialbd.ttf", 24)
        text_font = ImageFont.truetype("arial.ttf", 20)
    except:
        title_font = section_font = text_font = ImageFont.load_default()

    y_left = margin
    y_right = margin
    left_x = margin
    right_x = width // 2 + margin

    
    header_text = "Persona"
    bbox = title_font.getbbox(header_text)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((width - w) // 2, margin // 2), header_text, font=title_font, fill="black")

    
    draw.text((left_x, y_left), "👤 Name: DeltaRune", font=section_font, fill="black")
    y_left += spacing
    draw.text((left_x, y_left), "🎂 Age Range: 16–25 (estimated)", font=text_font, fill="black")
    y_left += spacing
    draw.text((left_x, y_left), "🧠 Archetype: The Enthusiast", font=text_font, fill="black")
    y_left += spacing

    sentiment = info["avg_sentiment"]
    sentiment_label = "Positive 😊" if sentiment > 0.2 else "Negative 😡" if sentiment < -0.2 else "Neutral 😐"
    emoji_label = "🎉 Frequent Emoji User" if info["emoji_count"] > 10 else "🧐 Minimal Emoji Use"

    draw.text((left_x, y_left), f"🗣️ Tone: {sentiment_label}", font=text_font, fill="black")
    y_left += spacing
    draw.text((left_x, y_left), f"📝 Avg Post Length: ~{int(info['avg_length'])} words", font=text_font, fill="black")
    y_left += spacing
    draw.text((left_x, y_left), f"💬 Behavior: {emoji_label}", font=text_font, fill="black")
    y_left += spacing

    
    draw.text((right_x, y_right), "🔑 Top Keywords", font=section_font, fill="black")
    y_right += spacing
    for word, freq in info["keywords"]:
        draw.text((right_x + 20, y_right), f"• {word} ({freq} times)", font=text_font, fill="black")
        y_right += spacing - 10

    y_right += spacing // 2
    draw.text((right_x, y_right), "😤 Frustrations", font=section_font, fill="black")
    y_right += spacing
    for f in info["frustrations"]:
        text_line = f[:70] + "..." if len(f) > 70 else f
        draw.text((right_x + 20, y_right), f"• {text_line}", font=text_font, fill="black")
        y_right += spacing - 10

    
    bottom = max(y_left, y_right) + margin
    img = img.crop((0, 0, width, bottom))

    img.save(filename)
    print(f"✅ Persona landscape resume image saved as: {filename}")
