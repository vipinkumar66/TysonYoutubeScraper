from pdf_generator import create_pdf_with_video_details
from get_transcription import YouTubeTranscription
import streamlit as st
from io import BytesIO
import time
import sys
import os

youtube_details_scraper = YouTubeTranscription()


# Redirect stdout to a custom stream that captures the output
class StreamCapturer:
    def __init__(self, output_func):
        self.output_func = output_func
        self.content = ""

    def write(self, text):
        self.content += text
        # Update Streamlit sidebar with the captured output
        self.output_func(self.content)


def download_pdf(pdf_content, filename):
    """Allow user to download the generated PDF file."""
    st.download_button(
        label="Download PDF",
        data=pdf_content,
        file_name=filename,
        mime='application/pdf'
    )


st.title('YouTube Scraper')

# Add title for application logs in the Streamlit sidebar
st.sidebar.title("Application Status:")

# Create a placeholder for verbose output in the Streamlit sidebar
verbose_placeholder = st.sidebar.empty()

# Input fields
youtube_url = st.text_area("YouTube Video URL:", placeholder="Enter YouTube Video URL")

if st.button('Submit'):

    # Redirect stdout to the custom stream capturer
    sys.stdout = StreamCapturer(verbose_placeholder.text)

    if not youtube_url:
        st.error("YouTube URL is required!")
    else:
        # Process the YouTube URL and generate the PDF
        try:
            # Generate PDF and store it in memory
            buffer = BytesIO()
            extracted_data = youtube_details_scraper.process_video_url(youtube_url)
            if extracted_data is not None:
                filename = create_pdf_with_video_details(extracted_data, buffer)

                # Provide an option to download the PDF
                buffer.seek(0)
                download_pdf(buffer, filename)
                st.success("Process completed. Check the sidebar for details.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Reset stdout to default
    sys.stdout = sys.__stdout__
