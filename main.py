from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from services.recommendation_service import generate_home_recommendations
from services.recommendation_service import generate_party_recommendations
from services.recommendation_service import generate_jewelry_recommendations
from services.gemini_service import generate_ai_recommendation

app = FastAPI(
    title="PocketSmart AI",
    description="Your Smart Budget & Recommendation Assistant",
    version="1.0.0"
)
# Temporary user storage
users = {}
recommendation_history = []
@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"request": request}
    )


@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"request": request}
    )

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@app.get("/home-planner")
async def home_planner(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home_planner.html",
        context={"request": request}
    )


@app.post("/generate-home")
async def generate_home(
    request: Request,
    budget: float = Form(...),
    room_type: str = Form(...),
    lights: int = Form(...),
    fans: int = Form(...),
    tables: int = Form(...)
):

    if budget <= 0:
        raise HTTPException(
            status_code=400,
            detail="Budget must be greater than zero."
        )

    if lights < 0 or fans < 0 or tables < 0:
        raise HTTPException(
            status_code=400,
            detail="Quantities cannot be negative."
        )

    if not room_type.strip():
        raise HTTPException(
            status_code=400,
            detail="Room type cannot be empty."
        )

    recommendations = generate_home_recommendations(
        budget,
        room_type,
        lights,
        fans,
        tables
    )

    prompt = f"""
    Suggest 3 affordable and practical home decoration ideas.

    Budget: ₹{budget}
    Room Type: {room_type}
    Lights: {lights}
    Fans: {fans}
    Tables: {tables}

    Give simple explanations and estimated costs.
    """

    ai_response = generate_ai_recommendation(prompt)

    # Save recommendation in history
    recommendation_history.append({
        "type": "Home Planner",
        "budget": budget,
        "details": f"Room: {room_type}",
        "ai_response": ai_response
    })

    return templates.TemplateResponse(
        request=request,
        name="home_result.html",
        context={
            "request": request,
            "budget": budget,
            "room_type": room_type,
            "lights": lights,
            "fans": fans,
            "tables": tables,
            "recommendations": recommendations,
            "ai_response": ai_response
        }
    )
@app.get("/party-planner")
async def party_planner(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="party_planner.html",
        context={"request": request}
    )


@app.post("/generate-party")
async def generate_party(
    request: Request,
    budget: float = Form(...),
    guests: int = Form(...),
    event_type: str = Form(...),
    venue: str = Form(...)
):

    if budget <= 0:
        raise HTTPException(
            status_code=400,
            detail="Budget must be greater than zero."
        )

    if guests <= 0:
        raise HTTPException(
            status_code=400,
            detail="Number of guests must be greater than zero."
        )

    if not event_type.strip() or not venue.strip():
        raise HTTPException(
            status_code=400,
            detail="Event type and venue cannot be empty."
        )

    recommendations = generate_party_recommendations(
        budget,
        guests,
        event_type,
        venue
    )

    prompt = f"""
    Suggest 3 affordable and practical ideas for a {event_type}.

    Budget: ₹{budget}
    Number of Guests: {guests}
    Venue: {venue}

    Suggest ideas for catering, decoration, and entertainment.
    Include estimated costs and simple explanations.
    """

    ai_response = generate_ai_recommendation(prompt)

    # Save party recommendation in history
    recommendation_history.append({
        "type": "Party Planner",
        "budget": budget,
        "details": f"Event: {event_type}, Guests: {guests}, Venue: {venue}",
        "ai_response": ai_response
    })

    return templates.TemplateResponse(
        request=request,
        name="party_result.html",
        context={
            "request": request,
            "budget": budget,
            "guests": guests,
            "event_type": event_type,
            "venue": venue,
            "recommendations": recommendations,
            "ai_response": ai_response
        }
    )

@app.get("/jewelry-planner")
async def jewelry_planner(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="jewelry_planner.html",
        context={"request": request}
    )


@app.post("/generate-jewelry")
async def generate_jewelry(
    request: Request,
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form(...),
    outfit_image: UploadFile = File(None)
):

    if budget <= 0:
        raise HTTPException(
            status_code=400,
            detail="Budget must be greater than zero."
        )

    if not occasion.strip() or not style.strip():
        raise HTTPException(
            status_code=400,
            detail="Occasion and style cannot be empty."
        )

    image_name = (
        outfit_image.filename
        if outfit_image and outfit_image.filename
        else "No image uploaded"
    )

    recommendations = generate_jewelry_recommendations(
        budget,
        occasion,
        style,
        image_name
    )

    prompt = f"""
    Suggest 3 affordable and stylish jewelry recommendations.

    Budget: ₹{budget}
    Occasion: {occasion}
    Style: {style}
    Outfit Image: {image_name}

    Suggest a necklace, earrings, and bracelet.
    Include estimated costs and simple explanations.
    """

    ai_response = generate_ai_recommendation(prompt)

    # Save jewelry recommendation in history
    recommendation_history.append({
        "type": "Jewelry Planner",
        "budget": budget,
        "details": f"Occasion: {occasion}, Style: {style}",
        "ai_response": ai_response
    })

    return templates.TemplateResponse(
        request=request,
        name="jewelry_result.html",
        context={
            "request": request,
            "budget": budget,
            "occasion": occasion,
            "style": style,
            "image_name": image_name,
            "recommendations": recommendations,
            "ai_response": ai_response
        }
    )
@app.post("/login")
async def login_user(
    email: str = Form(...),
    password: str = Form(...)
):
    if email in users and users[email]["password"] == password:
        return RedirectResponse(url="/", status_code=303)

    return {
        "message": "Invalid email or password"
    }
@app.post("/register")
async def register_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    users[email] = {
        "name": name,
        "password": password
    }

    return RedirectResponse(url="/login", status_code=303)

@app.get("/logout")
async def logout():
    return RedirectResponse(url="/", status_code=303)

@app.get("/startup")
async def startup():
    return {
        "status": "success",
        "message": "PocketSmart AI is running successfully!"
    }
@app.get("/recommendations-details", response_class=HTMLResponse)
async def recommendations_details(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="recommendations_details.html",
        context={
            "request": request,
            "history": recommendation_history
        }
    )
@app.get("/history", response_class=HTMLResponse)
async def history(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "request": request,
            "history": recommendation_history
        }
    )