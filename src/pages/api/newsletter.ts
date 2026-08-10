import type { APIRoute } from "astro";

const BUTTONDOWN_API_KEY = process.env.BUTTONDOWN_API_KEY;

export const prerender = false;

export const POST: APIRoute = async ({ request }) => {
  if (!BUTTONDOWN_API_KEY) {
    return new Response(
      JSON.stringify({ error: "Newsletter no configurado" }),
      { status: 503, headers: { "Content-Type": "application/json" } }
    );
  }

  try {
    const body = await request.json();
    const { email } = body;

    if (!email || typeof email !== "string" || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return new Response(
        JSON.stringify({ error: "Email no válido" }),
        { status: 400, headers: { "Content-Type": "application/json" } }
      );
    }

    const res = await fetch("https://api.buttondown.com/v1/subscribers", {
      method: "POST",
      headers: {
        Authorization: `Token ${BUTTONDOWN_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email_address: email,
        status: "active",
      }),
    });

    if (res.ok) {
      return new Response(
        JSON.stringify({ ok: true, message: "¡Suscrito correctamente!" }),
        { status: 200, headers: { "Content-Type": "application/json" } }
      );
    }

    const data = await res.json();

    if (data?.error?.includes("already")) {
      return new Response(
        JSON.stringify({ ok: true, message: "Ya estás suscrito" }),
        { status: 200, headers: { "Content-Type": "application/json" } }
      );
    }

    return new Response(
      JSON.stringify({ error: data?.error || "Error al suscribir" }),
      { status: res.status, headers: { "Content-Type": "application/json" } }
    );
  } catch {
    return new Response(
      JSON.stringify({ error: "Error del servidor" }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
};
