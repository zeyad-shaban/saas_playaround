// Next.js Route Handler
export async function GET() {
    const API_URL = process.env.NODE_ENV === "development"
        ? "http://127.0.0.1:8000/api/idea" // Local FastAPI
        : `/api/idea`;
        
    const response = await fetch(API_URL, {
        cache: 'no-store', // Ensures no intermediate caching
    });

    return new Response(response.body, {
        headers: {
            "Content-Type": "text/plain; charset=utf-8",
            "X-Accel-Buffering": "no",
            "Cache-Control": "no-cache",
        },
    });
}