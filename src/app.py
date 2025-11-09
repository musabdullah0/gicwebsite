from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import httpx
from datetime import datetime
import os

app = FastAPI()

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("src/index.html", "r") as f:
        return f.read()

@app.get("/api/prayer-times")
async def get_prayer_times():
    """Fetch prayer times from Masjidal API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://masjidal.com/api/v1/time/range?masjid_id=xwLVMDKJ",
                timeout=10.0
            )
            data = response.json()
            
        if data.get('data'):
            adhans = data['data']['salah'][0]
            iqamas = data['data']['iqamah'][0]
            
            # Format prayer times
            prayers = [
                {'name': 'Fajr', 'adhan': adhans.get('fajr', 'N/A'), 'iqama': iqamas.get('fajr', 'N/A')},
                {'name': 'Sunrise', 'adhan': adhans.get('sunrise', 'N/A'), 'iqama': None},
                {'name': 'Dhuhr', 'adhan': adhans.get('zuhr', 'N/A'), 'iqama': iqamas.get('zuhr', 'N/A')},
                {'name': 'Asr', 'adhan': adhans.get('asr', 'N/A'), 'iqama': iqamas.get('asr', 'N/A')},
                {'name': 'Maghrib', 'adhan': adhans.get('maghrib', 'N/A'), 'iqama': iqamas.get('maghrib', 'N/A')},
                {'name': 'Isha', 'adhan': adhans.get('isha', 'N/A'), 'iqama': iqamas.get('isha', 'N/A')},
            ]
            
            # Remove AM/PM for cleaner display
            for prayer in prayers:
                if prayer['adhan'] != 'N/A':
                    prayer['adhan'] = prayer['adhan'].replace(' AM', '').replace(' PM', '')
                if prayer['iqama'] and prayer['iqama'] != 'N/A':
                    prayer['iqama'] = prayer['iqama'].replace(' AM', '').replace(' PM', '')
            
            # Build HTML table
            html = f"""
            <div class="text-sm text-gray-600 mb-4 text-center">
                Updated: {datetime.now().strftime('%b %d, %Y')}
            </div>
            <div class="space-y-2">
                <div class="grid grid-cols-3 gap-4 pb-2 border-b-2 border-gray-200 font-semibold text-gray-700">
                    <div>Prayer</div>
                    <div class="text-center">Adhan</div>
                    <div class="text-center">Iqama</div>
                </div>
            """
            
            for prayer in prayers:
                iqama_text = prayer['iqama'] if prayer['iqama'] else '-'
                html += f"""
                <div class="grid grid-cols-3 gap-4 py-3 border-b border-gray-100 hover:bg-gray-50 transition">
                    <div class="font-semibold text-gray-800">{prayer['name']}</div>
                    <div class="text-center text-gray-600">{prayer['adhan']}</div>
                    <div class="text-center text-gray-600">{iqama_text}</div>
                </div>
                """
            
            html += "</div>"
            return HTMLResponse(content=html)
            
    except Exception as e:
        return HTMLResponse(
            content=f"""
            <div class="text-center py-8 text-red-600">
                <p>Unable to load prayer times at this moment.</p>
                <p class="text-sm mt-2">Please try again later.</p>
            </div>
            """,
            status_code=200
        )

@app.post("/api/newsletter")
async def newsletter_signup(email: str = Form(...)):
    """
    Newsletter signup endpoint
    In production, integrate with Mailchimp API using their credentials
    """
    # TODO: Add Mailchimp integration
    # You'll need to set environment variables:
    # MAILCHIMP_API_KEY and MAILCHIMP_LIST_ID
    
    # For now, return success message
    # In production, use the Mailchimp API:
    # https://mailchimp.com/developer/marketing/api/list-members/add-member-to-list/
    
    return HTMLResponse(
        content="""
        <p class="text-white font-semibold">✓ Thank you for subscribing!</p>
        <p class="text-green-100 text-sm">You'll receive updates about our programs and events.</p>
        """,
        status_code=200
    )

@app.post("/api/contact")
async def contact_form(
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...)
):
    """
    Contact form endpoint
    In production, this should send an email to admin@gicmasjid.org
    """
    # TODO: Add email sending functionality
    # You can use services like SendGrid, Amazon SES, or SMTP
    
    # Log the contact form submission
    print(f"Contact Form Submission:")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Subject: {subject}")
    print(f"Message: {message}")
    
    return HTMLResponse(
        content="""
        <div class="p-4 bg-green-50 border border-green-200 rounded-lg text-green-800">
            <p class="font-semibold">✓ Message sent successfully!</p>
            <p class="text-sm">We'll get back to you as soon as possible.</p>
        </div>
        """,
        status_code=200
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
