# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://main.dtf4ilvqx19lx.amplifyapp.com",  # ✅ Amplify frontend
        "http://localhost:3000"  # ✅ local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
