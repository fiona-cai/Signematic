# Signematic

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Node.js](https://img.shields.io/badge/Node.js-14%2B-green)
![Three.js](https://img.shields.io/badge/Three.js-0.126.0-lightgrey)
![Chrome](https://img.shields.io/badge/Chrome_Extension-v1.0-orange)
![Adobe Express](https://img.shields.io/badge/Adobe_Express-Integration-yellow)

## About This Project

**Signematic** aims to provide live sign language transcription for videos and movies using advanced machine-learning algorithms and gesture models. Our solution ensures that the deaf and hard-of-hearing community can enjoy a seamless viewing experience with accurate and real-time sign language interpretation.

## How We Built It

Signematic was developed using a combination of cutting-edge technologies:

- **Web Scraping**: Utilized Beautiful Soup to extract relevant sign language videos from the web.
- **Three.js**: Implemented for creating dynamic and realistic hand skeleton animations.
- **Node.js**: Used for backend development and managing server-side operations.
- **Speech Recognition**: Integrated for converting spoken words in videos into text.
- **YouTube Search Algorithms**: Employed to find and retrieve videos matching the speech-to-text output.

### Chrome Extension & Adobe Add-On

When a user enables the Signematic Chrome extension, it converts the speech in the video to text using a robust speech recognition engine. This text is processed by a web scraper that uses ASL grammar rules to search for videos depicting the corresponding signs. These videos are stitched together into a cohesive sign language interpretation overlay, providing a synchronized viewing experience. Additionally, Signematic is available as an Adobe add-on, enabling content creators to auto-generate sign language subtitles for their videos.

## Challenges Faced

- **Cross-Platform Integration**: Ensuring seamless communication between Adobe applications and our Python code proved to be a significant challenge.
- **Speech Recognition Accuracy**: Dealing with diverse accents and low-volume audio often resulted in missed or incorrect words, impacting the overall transcription quality.

## What We Learned

- **Three.js**: Gained proficiency in using Three.js to create efficient and accurate hand skeleton animations, which are critical for sign language depiction.
- **Adobe Express**: Explored and integrated our solution with Adobe Express, familiarizing ourselves with its user experience to effectively enhance content creation inclusivity.
- **Google Chrome Extensions**: Leveraged our prior experience in developing Chrome extensions to create a sophisticated solution that overlays animations and videos in the user's browser. The project is also launched on a VR headset, making video watching fully immersive.

## Next Steps

- **Social Media Integration**: We plan to implement our solution for popular social media platforms like Instagram, enabling creators to easily add sign language features without hassle.
- **Gesture Animation Enhancement**: We aim to improve the smoothness of the animations by slowing down the training videos and applying a smoothing effect to the movement of points and lines.
- **Language Expansion**: Currently utilizing ASL, we hope to expand our project to include other sign languages, such as BSL, in the future.
