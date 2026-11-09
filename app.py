import os
import tempfile
import streamlit as st
from src.qa import retrieve_context, generate_answer
from src.document_manager import process_and_store_pdf, list_documents, delete_document
from src.summarizer import summarize_chunks
from src.vector_store import get_document_chunks
from src.auth import init_auth_db
from src.auth_ui import render_auth_page

st.set_page_config(
    page_title="StudyMate AI",
    page_icon="📚",
    layout="wide"
)

st.markdown("""
<style>

/* MAIN APPLICATION THEME */

.stApp {
    background: radial-gradient(
        circle at 50% 0%,
        #101B35 0%,
        #090F1F 45%,
        #070B16 100%
    );
    color: #F1F5F9;
}

[data-testid="stAppViewContainer"] {
    background: transparent;
}

[data-testid="stHeader"] {
    background: rgba(7, 11, 22, 0.7);
}

.block-container {
    max-width: 1100px;
    padding-top: 4rem;
    padding-bottom: 5rem;
}


/


/* =================================
   SIDEBAR - REFINED DESIGN
================================= */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0B1425,
        #101D32
    );
    border-right: 1px solid rgba(71, 85, 105, 0.25);
}

[data-testid="stSidebar"] > div:first-child {
    padding: 24px 18px;
}

/* BRANDING */

.sidebar-title {
    color: #F1F5F9;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.6px;
    text-align: left;
    margin: 0;
}

.sidebar-subtitle {
    color: #94A3B8;
    font-size: 11px;
    text-align: left;
    margin-top: 3px;
    margin-bottom: 24px;
}

/* WORKSPACE */

.sidebar-section-label {
    color: #64748B;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.4px;
    margin: 10px 0 12px 8px;
}

/* NAVIGATION BUTTONS */

[data-testid="stSidebar"] [class*="st-key-sidebar_nav_item"] button {
    background: transparent !important;
    color: #CBD5E1 !important;
    border: 1px solid transparent !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    text-align: left !important;
    min-height: 43px;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] [class*="st-key-sidebar_nav_item"] button:hover {
    background: rgba(37, 99, 235, 0.12) !important;
    color: #67E8F9 !important;
}

/* ACTIVE BUTTON */

[data-testid="stSidebar"] [class*="st-key-sidebar_nav_active"] button {
    background: rgba(37, 99, 235, 0.20) !important;
    color: #67E8F9 !important;
    border: 1px solid rgba(34, 211, 238, 0.25) !important;
    font-weight: 600 !important;
}

/* FOOTER */

.sidebar-footer {
    color: #64748B;
    font-size: 10px;
    text-align: center;
    margin-top: 28px;
    padding-top: 14px;
    border-top: 1px solid rgba(71, 85, 105, 0.2);
}

/* LEFT ALIGN SIDEBAR NAVIGATION TEXT */

[data-testid="stSidebar"] [class*="st-key-sidebar_button"] button {
    justify-content: flex-start !important;
    text-align: left !important;
}

[data-testid="stSidebar"] [class*="st-key-sidebar_button"] button > div {
    width: 100%;
    justify-content: flex-start !important;
}

/* ANIMATED WELCOME HEADING */

@keyframes fadeSlideUp {

    from {
        opacity: 0;
        transform: translateY(25px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }

}

.hero-heading {
    text-align: center;
    color: #F1F5F9;
    font-size: 32px;
    font-weight: 650;
    letter-spacing: -0.8px;
    line-height: 1.3;
    margin-top: 45px;
    margin-bottom: 8px;
    animation: fadeSlideUp 0.8s ease-out;
}

.hero-subtitle {
    text-align: center;
    color: #94A3B8;
    font-size: 15px;
    font-weight: 400;
    line-height: 1.6;
    margin-top: 0;
    margin-bottom: 28px;
    animation: fadeSlideUp 1s ease-out;
    animation-fill-mode: both;
}



/* =================================
   CHAT MESSAGE CARDS
================================= */

[data-testid="stChatMessage"] {
    background: rgba(18, 31, 54, 0.85);
    border: 1px solid #263B5C;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 16px;
    transition: border-color 0.25s ease;
}

/* USER MESSAGE */

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: rgba(29, 78, 216, 0.10);
    border-color: rgba(59, 130, 246, 0.35);
}

/* AI MESSAGE */

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: rgba(18, 31, 54, 0.9);
    border-color: rgba(8, 145, 178, 0.3);
}

/* HOVER EFFECT */

[data-testid="stChatMessage"]:hover {
    border-color: #0891B2;
}

/* MESSAGE TEXT */

[data-testid="stChatMessage"] p {
    color: #E2E8F0;
    font-size: 15px;
    line-height: 1.8;
    margin-bottom: 12px;
}

/* RESPONSE HEADINGS */

[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3 {
    color: #67E8F9;
    line-height: 1.4;
    margin-top: 18px;
    margin-bottom: 12px;
}

/* BOLD TEXT */

[data-testid="stChatMessage"] strong {
    color: #F8FAFC;
    font-weight: 650;
}

/* BULLET AND NUMBERED LISTS */

[data-testid="stChatMessage"] ul,
[data-testid="stChatMessage"] ol {
    padding-left: 24px;
    margin-top: 8px;
    margin-bottom: 14px;
}

[data-testid="stChatMessage"] li {
    color: #E2E8F0;
    line-height: 1.8;
    padding-left: 4px;
    margin-bottom: 6px;
}

/* CODE BLOCKS */

[data-testid="stChatMessage"] pre {
    background: #0B1425 !important;
    border: 1px solid #294365;
    border-radius: 12px;
    padding: 16px;
    margin: 12px 0;
}

[data-testid="stChatMessage"] code {
    color: #67E8F9;
    font-size: 13px;
}


/* TABLES - RESPONSIVE DESIGN */

[data-testid="stChatMessage"] table {
    display: block;
    width: 100%;
    max-width: 100%;
    overflow-x: auto;
    border-collapse: collapse;
    border: 1px solid #294365;
    table-layout: auto;
}

[data-testid="stChatMessage"] th {
    background: #1B2D49;
    color: #67E8F9;
    padding: 12px;
    text-align: left;
    white-space: normal;
    min-width: 110px;
}

[data-testid="stChatMessage"] td {
    color: #E2E8F0;
    padding: 12px;
    border: 1px solid #294365;
    min-width: 110px;
    overflow-wrap: anywhere;
    vertical-align: top;
}

/* MOBILE TABLE IMPROVEMENTS */

@media screen and (max-width: 480px) {

    [data-testid="stChatMessage"] table {
        display: block;
        width: 100%;
        max-width: 100%;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }

    [data-testid="stChatMessage"] th,
    [data-testid="stChatMessage"] td {
        min-width: 110px;
        padding: 9px;
        font-size: 13px;
        line-height: 1.6;
    }

}

/* FIX AI RESPONSE CONTENT ALIGNMENT */

@media screen and (max-width: 480px) {

    [data-testid="stChatMessage"] {
        width: 100% !important;
        box-sizing: border-box !important;
        padding: 14px !important;
        overflow: hidden;
    }

    [data-testid="stChatMessage"] [data-testid="stChatMessageContent"] {
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }

    [data-testid="stChatMessage"] [data-testid="stMarkdown"] {
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }

}

/* CHAT INPUT */

[data-testid="stChatInput"] {
    background: #111D32;
    border: 1px solid #294365;
    border-radius: 18px;
    transition: all 0.2s ease;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #22D3EE;
    box-shadow: 0 0 15px rgba(34, 211, 238, 0.12);
}

[data-testid="stChatInput"] textarea {
    color: #F1F5F9;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #8293AA;
}


/* TEXT INPUTS AND SELECT BOXES */

.stTextInput input,
.stTextArea textarea,
.stSelectbox [data-baseweb="select"] > div {
    background: #111D32;
    color: #F1F5F9;
    border-color: #294365;
    border-radius: 10px;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #22D3EE;
    box-shadow: 0 0 10px rgba(34, 211, 238, 0.12);
}


/* MODE SELECTOR */

[data-testid="stSegmentedControl"] {
    background: #111D32;
    border: 1px solid #294365;
    border-radius: 12px;
    padding: 5px;
}

[data-testid="stSegmentedControl"] button {
    color: #AFC1D8;
    border-radius: 8px;
}

[data-testid="stSegmentedControl"] button[aria-pressed="true"] {
    background: linear-gradient(
        135deg,
        #2563EB,
        #0891B2
    ) !important;
    color: #FFFFFF !important;
    border: 1px solid #22D3EE !important;
    box-shadow: 0 0 12px rgba(34, 211, 238, 0.2);
}


/* BUTTONS */

.stButton button,
.stFormSubmitButton button {
    background: linear-gradient(
        135deg,
        #2563EB,
        #0891B2
    );
    color: #FFFFFF;
    border: 1px solid #3186D8;
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    background: linear-gradient(
        135deg,
        #1D4ED8,
        #0E7490
    );
    border-color: #22D3EE;
    color: #FFFFFF;
    box-shadow: 0 0 15px rgba(34, 211, 238, 0.18);
    transform: translateY(-1px);
}


/* DIVIDERS */

hr {
    border-color: #1E3152;
}


/* GENERAL TEXT */

h1, h2, h3 {
    color: #F1F5F9;
}

p {
    color: #CBD5E1;
}


/* SCROLLBAR */

::-webkit-scrollbar {
    width: 7px;
}

::-webkit-scrollbar-track {
    background: #090F1F;
}

::-webkit-scrollbar-thumb {
    background: #294365;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #2563EB;
}


/* =================================
   CHAT COMPOSER
================================= */

/* MAIN INPUT CONTAINER */

[data-testid="stForm"] {
    background: rgba(17, 29, 50, 0.92);
    border: 1px solid #294365;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 5px 25px rgba(0, 0, 0, 0.2);
    transition: all 0.25s ease;
}

/* FOCUS EFFECT */

[data-testid="stForm"]:focus-within {
    border-color: #2563EB;
    box-shadow: 0 0 20px rgba(37, 99, 235, 0.18);
}

/* TEXT INPUT */

[data-testid="stForm"] textarea {
    background: transparent !important;
    color: #F1F5F9 !important;
    border: none !important;
    box-shadow: none !important;
    font-size: 15px;
    line-height: 1.7;
    padding: 10px;
    resize: vertical;
}

/* PLACEHOLDER */

[data-testid="stForm"] textarea::placeholder {
    color: #8293AA !important;
    opacity: 1;
}

/* SEND BUTTON */

[data-testid="stForm"] button {
    background: linear-gradient(135deg, #2563EB, #0891B2);
    color: #FFFFFF;
    border: none;
    border-radius: 11px;
    padding: 8px 22px;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.25s ease;
}

/* BUTTON HOVER */

[data-testid="stForm"] button:hover {
    background: linear-gradient(135deg, #1D4ED8, #0E7490);
    box-shadow: 0 0 16px rgba(34, 211, 238, 0.25);
    transform: translateY(-2px);
}

/* BUTTON ACTIVE */

[data-testid="stForm"] button:active {
    transform: translateY(0);
    box-shadow: none;
}

/* INPUT FOCUS */

[data-testid="stForm"] textarea:focus {
    outline: none !important;
    box-shadow: none !important;
}

    
/* CHAT MESSAGE CONTAINER */

[data-testid="stChatMessage"] {
    padding: 18px 20px;
    border-radius: 16px;
    margin-bottom: 14px;
    border: 1px solid rgba(71, 85, 105, 0.25);
    transition: all 0.2s ease;
}


/* USER MESSAGE */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {
    background: linear-gradient(
        135deg,
        rgba(37, 99, 235, 0.16),
        rgba(8, 145, 178, 0.10)
    );
    border-color: rgba(37, 99, 235, 0.35);
}


/* AI MESSAGE */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {
    background: rgba(17, 29, 50, 0.75);
    border-color: rgba(34, 211, 238, 0.20);
}


/* MESSAGE TEXT */

[data-testid="stChatMessage"] p {
    color: #E2E8F0;
    line-height: 1.7;
    font-size: 15px;
}


/* MESSAGE HOVER */

[data-testid="stChatMessage"]:hover {
    border-color: rgba(34, 211, 238, 0.4);
}


}

/* SUMMARY HERO */

.summary-hero {
    text-align: center;
    padding: 25px 20px;
    margin: 10px 0 25px 0;
}

.summary-hero h2 {
    color: #F1F5F9;
    font-size: 30px;
    font-weight: 700;
    margin-bottom: 10px;
}

.summary-hero p {
    color: #94A3B8;
    font-size: 15px;
    margin: 0;
}

/* SUMMARY SUCCESS MESSAGE */

.summary-success {
    background: rgba(8, 145, 178, 0.12);
    border: 1px solid rgba(34, 211, 238, 0.3);
    border-radius: 12px;
    padding: 16px 20px;
    color: #67E8F9;
    font-size: 15px;
    font-weight: 500;
    margin: 15px 0;
}

.summary-success span {
    color: #22D3EE;
    font-weight: 700;
    margin-right: 10px;
}

/* GENERATED SUMMARY CONTAINER */

.st-key-summary_output {
    background: rgba(17, 29, 50, 0.75);
    border: 1px solid rgba(34, 211, 238, 0.22);
    border-radius: 16px;
    padding: 24px;
    margin-top: 15px;
    box-shadow: 0 5px 25px rgba(0, 0, 0, 0.15);
}


/* SUMMARY HEADINGS */

.st-key-summary_output h1,
.st-key-summary_output h2,
.st-key-summary_output h3 {
    color: #67E8F9;
    font-weight: 650;
    margin-top: 20px;
    margin-bottom: 12px;
}


/* SUMMARY TEXT */

.st-key-summary_output p,
.st-key-summary_output li {
    color: #E2E8F0;
    font-size: 15px;
    line-height: 1.8;
}


/* SUMMARY BOLD TEXT */

.st-key-summary_output strong {
    color: #FFFFFF;
}

/* UPLOAD PAGE HERO */

.upload-hero {
    text-align: center;
    padding: 25px 20px;
    margin: 10px 0 30px 0;
}

.upload-hero h2 {
    color: #F1F5F9;
    font-size: 30px;
    font-weight: 700;
    margin-bottom: 10px;
}

.upload-hero p {
    color: #94A3B8;
    font-size: 15px;
    margin: 0;
}


/* =================================
   MY MATERIALS - UPLOAD PAGE
================================= */

/* PAGE HERO */

.upload-hero {
    text-align: center;
    margin-top: 30px;
    margin-bottom: 30px;
    animation: fadeSlideUp 0.8s ease-out;
}

.upload-hero h2 {
    color: #F1F5F9;
    font-size: 32px;
    font-weight: 650;
    letter-spacing: -0.7px;
    margin-bottom: 10px;
}

.upload-hero p {
    color: #94A3B8;
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 0;
}

/* PDF UPLOAD AREA */

[data-testid="stFileUploader"] {
    background: rgba(17, 29, 50, 0.8);
    border: 1px dashed rgba(34, 211, 238, 0.45);
    border-radius: 18px;
    padding: 22px;
    transition: all 0.25s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: #2563EB;
    background: rgba(37, 99, 235, 0.08);
    box-shadow: 0 0 18px rgba(8, 145, 178, 0.10);
}

[data-testid="stFileUploader"] section {
    background: transparent;
}

[data-testid="stFileUploader"] small {
    color: #94A3B8;
}

[data-testid="stFileUploader"] label {
    color: #E2E8F0;
}

/* BROWSE FILE BUTTON */

[data-testid="stFileUploader"] button {
    background: linear-gradient(135deg, #2563EB, #0891B2) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.25s ease;
}

[data-testid="stFileUploader"] button:hover {
    background: linear-gradient(135deg, #1D4ED8, #0E7490) !important;
    box-shadow: 0 0 15px rgba(34, 211, 238, 0.25) !important;
    transform: translateY(-1px);
}

/* SELECTED FILE INFORMATION */

[data-testid="stFileUploaderFile"] {
    background: rgba(18, 31, 54, 0.85);
    border: 1px solid #294365;
    border-radius: 10px;
}

/* PROCESS PDF BUTTON */

.st-key-process_pdf_button button {
    background: linear-gradient(135deg, #2563EB, #0891B2) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 11px !important;
    font-weight: 600 !important;
    padding: 10px 22px;
    transition: all 0.25s ease;
}

.st-key-process_pdf_button button:hover {
    background: linear-gradient(135deg, #1D4ED8, #0E7490) !important;
    box-shadow: 0 0 16px rgba(34, 211, 238, 0.25);
    transform: translateY(-2px);
}

/* STORED DOCUMENTS HEADING */

.st-key-document_section_title {
    color: #E2E8F0;
}

/* DOCUMENT CARDS */

[class*="st-key-document_card_"] {
    background: rgba(17, 29, 50, 0.82);
    border: 1px solid #294365;
    border-radius: 15px;
    padding: 8px 14px;
    margin-bottom: 12px;
    transition: all 0.25s ease;
}

[class*="st-key-document_card_"]:hover {
    border-color: rgba(8, 145, 178, 0.65);
    box-shadow: 0 0 16px rgba(8, 145, 178, 0.10);
}

/* DOCUMENT CARD TEXT */

[class*="st-key-document_card_"] p {
    color: #E2E8F0;
    line-height: 1.5;
}

[class*="st-key-document_card_"] strong {
    color: #F1F5F9;
    font-size: 15px;
    font-weight: 600;
}

[class*="st-key-document_card_"] small {
    color: #94A3B8;
}

/* DELETE BUTTON */

[class*="st-key-delete_"] button {
    background: rgba(220, 38, 38, 0.12) !important;
    color: #F87171 !important;
    border: 1px solid rgba(248, 113, 113, 0.4) !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease;
}

[class*="st-key-delete_"] button:hover {
    background: rgba(220, 38, 38, 0.25) !important;
    border-color: #F87171 !important;
    box-shadow: 0 0 12px rgba(220, 38, 38, 0.15);
}

/* UPLOAD PAGE DIVIDER */

[data-testid="stDivider"] {
    border-color: rgba(71, 85, 105, 0.35);
}


/* =================================
   PDF SELECTOR SECTION
================================= */

.pdf-selector-card {
    text-align: center;
    margin-top: 15px;
    margin-bottom: 12px;
}

.pdf-selector-title {
    color: #E2E8F0;
    font-size: 19px;
    font-weight: 600;
    letter-spacing: -0.3px;
}

/* PDF DROPDOWN */

.st-key-dashboard_document_selector [data-baseweb="select"] {
    background: rgba(17, 29, 50, 0.9);
    border: 1px solid #294365;
    border-radius: 12px;
    min-height: 48px;
    transition: all 0.25s ease;
}

/* HOVER EFFECT */

.st-key-dashboard_document_selector [data-baseweb="select"]:hover {
    border-color: #0891B2;
    box-shadow: 0 0 12px rgba(8, 145, 178, 0.15);
}

/* SELECTED DOCUMENT TEXT */

.st-key-dashboard_document_selector [data-baseweb="select"] span {
    color: #E2E8F0;
    font-size: 14px;
}

/* DROPDOWN ARROW */

.st-key-dashboard_document_selector [data-baseweb="select"] svg {
    fill: #94A3B8;
}

/* DROPDOWN OPTIONS */

[data-baseweb="popover"] {
    background: #111D32;
    border: 1px solid #294365;
    border-radius: 12px;
    overflow: hidden;
}

[data-baseweb="menu"] {
    background: #111D32;
}

[data-baseweb="menu"] li {
    color: #E2E8F0;
    font-size: 14px;
    transition: background 0.2s ease;
}

[data-baseweb="menu"] li:hover {
    background: rgba(37, 99, 235, 0.2);
}

/* SELECTED OPTION */

[data-baseweb="menu"] li[aria-selected="true"] {
    background: rgba(37, 99, 235, 0.25);
    color: #67E8F9;
}


/* =================================
   SELECTED PDF FILE CARD
================================= */

.selected-file-card {
    display: flex;
    align-items: center;
    gap: 14px;
    background: rgba(17, 29, 50, 0.85);
    border: 1px solid rgba(34, 211, 238, 0.25);
    border-radius: 13px;
    padding: 15px 18px;
    margin: 15px 0;
    transition: all 0.25s ease;
}

.selected-file-card:hover {
    border-color: rgba(34, 211, 238, 0.55);
    box-shadow: 0 0 15px rgba(8, 145, 178, 0.10);
}

.selected-file-icon {
    font-size: 25px;
}

.selected-file-info {
    flex: 1;
    min-width: 0;
}

.selected-file-name {
    color: #F1F5F9;
    font-size: 14px;
    font-weight: 600;
    overflow-wrap: anywhere;
}

.selected-file-status {
    color: #94A3B8;
    font-size: 11px;
    margin-top: 4px;
}

.selected-file-check {
    color: #34D399;
    font-size: 19px;
    font-weight: 700;
}

/* =================================
   PDF PROCESSING SUCCESS CARD
================================= */

.processing-success-card {
    background: rgba(16, 45, 48, 0.65);
    border: 1px solid rgba(52, 211, 153, 0.35);
    border-radius: 15px;
    padding: 22px;
    margin: 18px 0;
}

.success-icon {
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(52, 211, 153, 0.15);
    border-radius: 50%;
    color: #34D399;
    font-size: 23px;
    font-weight: 700;
    margin-bottom: 12px;
}

.success-title {
    color: #6EE7B7;
    font-size: 17px;
    font-weight: 650;
}

.success-description {
    color: #A7B9C7;
    font-size: 12px;
    margin-top: 5px;
    margin-bottom: 18px;
}

.success-details {
    border-top: 1px solid rgba(52, 211, 153, 0.18);
    padding-top: 14px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.success-details div {
    display: flex;
    justify-content: space-between;
    gap: 12px;
}

.success-details span {
    color: #94A3B8;
    font-size: 12px;
}

.success-details strong {
    color: #E2E8F0;
    font-size: 12px;
    font-weight: 600;
    text-align: right;
    overflow-wrap: anywhere;
}


/* =================================
   DUPLICATE PDF WARNING CARD
================================= */

.duplicate-warning-card {
    background: rgba(51, 40, 18, 0.65);
    border: 1px solid rgba(251, 191, 36, 0.3);
    border-radius: 15px;
    padding: 20px;
    margin: 18px 0;
}

.duplicate-icon {
    width: 34px;
    height: 34px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(251, 191, 36, 0.15);
    border-radius: 50%;
    color: #FBBF24;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 12px;
}

.duplicate-title {
    color: #FCD34D;
    font-size: 16px;
    font-weight: 650;
}

.duplicate-description {
    color: #B6A98C;
    font-size: 12px;
    line-height: 1.6;
    margin-top: 6px;
}

.duplicate-filename {
    color: #E2E8F0;
    background: rgba(251, 191, 36, 0.08);
    border-radius: 8px;
    padding: 10px;
    margin-top: 14px;
    font-size: 12px;
    overflow-wrap: anywhere;
}

/* MOBILE AI RESPONSE IMPROVEMENTS */

@media screen and (max-width: 480px) {

    /* RESPONSE HEADINGS */

    [data-testid="stChatMessage"] h1 {
        font-size: 23px !important;
        line-height: 1.4 !important;
    }

    [data-testid="stChatMessage"] h2 {
        font-size: 20px !important;
        line-height: 1.45 !important;
    }

    [data-testid="stChatMessage"] h3 {
        font-size: 18px !important;
        line-height: 1.5 !important;
    }

    /* RESPONSE PARAGRAPHS */

    [data-testid="stChatMessage"] p {
        font-size: 14px !important;
        line-height: 1.7 !important;
    }

    /* LISTS */

    [data-testid="stChatMessage"] li {
        font-size: 14px !important;
        line-height: 1.7 !important;
    }

    [data-testid="stChatMessage"] ul,
    [data-testid="stChatMessage"] ol {
        padding-left: 20px;
    }

    /* CODE BLOCKS */

    [data-testid="stChatMessage"] pre {
        max-width: 100%;
        overflow-x: auto;
        box-sizing: border-box;
    }

}
</style>
""", unsafe_allow_html=True)

# AUTHENTICATION INITIALIZATION

init_auth_db()

if "authenticated_user" not in st.session_state:
    st.session_state.authenticated_user = None

# SHOW LOGIN PAGE IF USER IS NOT LOGGED IN

if not st.session_state.authenticated_user:

    render_auth_page()

    st.stop()

# CURRENT USER INFORMATION

current_user = st.session_state.authenticated_user
current_user_id = str(current_user["user_id"])


# LEFT SIDEBAR

if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Home"

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-title">📚 StudyMate AI</div>
        <div class="sidebar-subtitle">
            Your Personal Study Assistant
        </div>
        """,
        unsafe_allow_html=True
    )

    # WORKSPACE LABEL
    st.markdown(
        '<div class="sidebar-section-label">WORKSPACE</div>',
        unsafe_allow_html=True
    )

    # NAVIGATION OPTIONS
    navigation_items = [
        ("Home", "⌂"),
        ("My Materials", "▤")
    ]

    for nav_label, nav_icon in navigation_items:

        is_active = (
            st.session_state.selected_page == nav_label
        )

        container_style = (
            "sidebar_nav_active"
            if is_active
            else "sidebar_nav_item"
        )

        with st.container(
            key=f"{container_style}_{nav_label.lower().replace(' ', '_')}"
        ):

            if st.button(
                f"{nav_icon}   {nav_label}",
                key=f"sidebar_button_{nav_label.lower().replace(' ', '_')}",
                use_container_width=True
            ):

                st.session_state.selected_page = nav_label
                st.rerun()

    # SIDEBAR FOOTER

        # LOGGED-IN USER INFORMATION

    st.divider()

    st.markdown(
        f"**👤 {current_user['name']}**"
    )

    st.caption(current_user["email"])

    # LOGOUT BUTTON

    if st.button(
        "↪ Log Out",
        key="logout_button",
        use_container_width=True
    ):

        st.session_state.authenticated_user = None

        st.session_state.messages = []
        st.session_state.summary = None
        st.session_state.summary_document_id = None

        st.rerun()
    
    st.markdown(
        """
        <div class="sidebar-footer">
            ✦ AI-powered learning workspace
        </div>
        """,
        unsafe_allow_html=True
    )


# PAGE MAPPING
page_mapping = {
    "Home": "Dashboard",
    "My Materials": "Upload PDF"
}

page = page_mapping[st.session_state.selected_page]


#CHAT HISTORY

if "messages" not in st.session_state:

    st.session_state.messages = []

if "summary" not in st.session_state:
    st.session_state.summary = None

if "summary_document_id" not in st.session_state:
    st.session_state.summary_document_id = None

#MAIN CHAT INTERFACE

if page in ["Dashboard", "Ask Questions"]:
    selected_document_id = None

# AI WORKSPACE MODE SELECTOR


if page == "Dashboard":

    # WORKSPACE MODE SELECTOR

    left, center, right = st.columns([2, 3, 2])

    with center:
        mode = st.segmented_control(
            "Workspace Mode",
            options=["Ask AI", "Summary"],
            default="Ask AI",
            label_visibility="collapsed",
            width="stretch",
            key = "dashboard_mode_selector"
        )

    documents = list_documents(current_user_id)

    selected_document = None
    selected_document_id = None


    # ASK AI MODE

    if mode == "Ask AI":

        # WELCOME HEADING

        if not st.session_state.messages:

            import html

            first_name = html.escape(
                st.session_state.authenticated_user["name"].split()[0]
            )

            st.markdown(f"""
            <div class="hero-heading">
                Welcome back, {first_name}! ✨
            </div>

            <div class="hero-subtitle">
                Your notes, your questions,
                your personal AI study companion.
            </div>
            """, unsafe_allow_html=True)


    # SUMMARY MODE

    elif mode == "Summary":

        st.markdown(
            """
            <div class="summary-hero">
                <h2>✨ Generate Your Summary</h2>
                <p>
                    Transform your study material into clear,
                    organized revision notes.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


    # SHARED PDF SELECTOR

    st.markdown("""
    <div class="pdf-selector-card">
        <div class="pdf-selector-title">
            📚 Select From Your Study Material
        </div>
    </div>
    """, unsafe_allow_html=True)

    if documents:

        selected_document = st.selectbox(
            "Select Your Study Material",
            options=documents,
            format_func=lambda doc: doc['filename'],
            label_visibility="collapsed",
            key="dashboard_document_selector"
        )

        selected_document_id = selected_document['document_id']

    else:

        st.info("Please upload a PDF first.")


    # ASK AI CHAT INTERFACE

    if mode == "Ask AI":

        # DISPLAY CHAT HISTORY

        for message in st.session_state.messages:

            with st.chat_message(message["role"]):

                st.markdown(message["content"])


        # FULL-WIDTH CHAT COMPOSER

        with st.form("chat_form", clear_on_submit=True):

            question = st.text_area(
                "Message",
                placeholder="Ask anything about your study material...",
                height=90,
                label_visibility="collapsed"
            )

            submitted = st.form_submit_button(
                "↑ Send",
                use_container_width=True
            )

            if submitted and question.strip():

                user_question = question.strip()

                st.session_state.messages.append({
                    "role": "user",
                    "content": user_question,
                })

                try:

                    with st.spinner("StudyMate AI is thinking..."):

                        retrieved_docs = retrieve_context(
                            question=user_question,
                            user_id = current_user_id,
                            document_id=selected_document_id,
                            k=4
                        )

                        answer = generate_answer(
                            question=user_question,
                            retrieved_docs=retrieved_docs,
                            chat_history=st.session_state.messages[:-1]
                        )

                        print("\nRAW ANSWER:\n", answer)

                        print(f"\nANSWER LENGTH: {len(answer)}")
                        print(f"\nANSWER END: {repr(answer[-200:])}")

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer
                        })
                except Exception as error:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Something went wrong: {error}"
                    })

                st.rerun()


    # SUMMARY GENERATION

    elif mode == "Summary":
        if selected_document:
            left, center, right = st.columns([1, 2, 1])
            with center:

                generate_clicked = st.button(
                    "Generate Summary",
                    use_container_width=True
                )

                if generate_clicked:
                    with st.spinner("Generating your summary..."):
                        try:
                            chunks = get_document_chunks(
                                document_id = selected_document_id,
                                user_id = current_user_id)
                            st.session_state.summary = summarize_chunks(chunks)
                            st.session_state.summary_document_id = selected_document_id
                            st.markdown(
                                """
                                <div class="summary-success">
                                    <span>✓</span>
                                    Summary generated successfully!
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        except Exception as error:
                            st.error(f"Unable to generate summary: {error}")
                if (
                    st.session_state.summary
                    and st.session_state.summary_document_id == selected_document_id
                ):
                    st.divider()
                    st.markdown("### 📖 Your Revision Notes")
                    with st.container(border=True, key="summary_output"):
                        st.markdown(st.session_state.summary)


#OTHER APPLICATION PAGES



elif page == "Upload PDF":

    # PAGE HEADING

    st.markdown(
        """
        <div class="upload-hero">
            <h2>📂 Your Study Materials</h2>
            <p>
                Upload, organize and manage your study documents
                in one place.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # PDF UPLOAD

    uploaded_file = st.file_uploader(
        "Choose a PDF File",
        type=["pdf"]
    )

    if uploaded_file is not None:

        st.markdown(
        f"""
        <div class="selected-file-card">
            <div class="selected-file-icon">📄</div>
            <div class="selected-file-info">
                <div class="selected-file-name">{uploaded_file.name}</div>
                <div class="selected-file-status">
                    PDF selected successfully ✓
                </div>
            </div>
            <div class="selected-file-check"></div>
        </div>
        """,
        unsafe_allow_html=True
        )

        if st.button(
            "Process PDF",
            key="process_pdf_button"
        ):
            temp_path = None

            try:

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as temp_file:

                    temp_file.write(uploaded_file.getbuffer())

                    temp_path = temp_file.name

                st.success("PDF File Uploaded Successfully")

                with st.spinner("Processing your PDF... Please wait."):

                    result = process_and_store_pdf(
                        pdf_path=temp_path,
                        filename=uploaded_file.name,
                        user_id=current_user_id
                    )
                if result.get("duplicate"):

                    st.markdown(
                        f"""
                        <div class="duplicate-warning-card">
                            <div class="duplicate-icon">!</div>
                            <div class="duplicate-title">
                                Document Already Exists
                            </div>
                            <div class="duplicate-description">
                                This PDF has already been uploaded.
                                You can access it from My Materials.
                            </div>
                            <div class="duplicate-filename">
                                📄 {result['filename']}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:
                    st.markdown(
                        f"""
                        <div class="processing-success-card">
                            <div class="success-icon">✓</div>
                            <div class="success-title">
                                PDF Processed Successfully!
                            </div>
                            <div class="success-description">
                                Your study material is ready to use.
                            </div>
                            <div class="success-details">
                                <div>
                                    <span>Filename</span>
                                    <strong>{result['filename']}</strong>
                                </div>
                                <div>
                                    <span>Total Pages</span>
                                    <strong>{result['total_pages']}</strong>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            except Exception as error:

                st.markdown(
                    f"""
                    <div class="processing-error-card">
                        <div class="error-icon">✕</div>
                        <div class="error-title">
                            PDF Processing Failed
                        </div>
                        <div class="error-description">
                            We couldn't process your document.
                            Please check the file and try again.
                        </div>
                        <div class="error-details">
                            {error}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            finally:
                            
                if temp_path and os.path.exists(temp_path):

                    os.remove(temp_path)

    st.divider()

    # STORED DOCUMENTS

    st.markdown("### 📚 Stored Documents")

    documents = list_documents(current_user_id)

    if not documents:

        st.info("No documents uploaded yet.")

    else:

        for doc in documents:

            with st.container(
                border=True,
                key=f"document_card_{doc['document_id']}"
            ):

                col1, col2 = st.columns([5, 1])

                with col1:

                    st.markdown(
                        f"📄 **{doc['filename']}**"
                    )

                    st.caption(
                        f"Total Pages: {doc['total_pages']}"
                    )

                with col2:

                    if st.button(
                        "Delete",
                        key=f"delete_{doc['document_id']}"
                    ):

                        delete_document(
                            document_id = doc["document_id"],
                            user_id = current_user_id)

                        st.success("Document deleted successfully!")

                        st.rerun()


