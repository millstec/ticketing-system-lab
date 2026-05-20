from flask import Flask, jsonify, request
import logging

# Create Flask application instance
app = Flask(__name__)

# ----------------------------
# Logging Configuration
# ----------------------------
# This configures how logs appear in the terminal.
# level=logging.INFO means we show INFO, WARNING, ERROR, CRITICAL
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ----------------------------
# In-memory data store (temporary database)
# Each ticket is a dictionary:
# {
#   "id": int,
#   "title": str,
#   "status": str
# }
# ----------------------------
tickets: list[dict[str, str | int]] = []


@app.route("/", methods=["GET"])
def home() -> tuple[dict, int]:
    """
    Root endpoint.
    Used to confirm service is running.
    """
    return {"service": "ticketing-system-lab", "status": "running"}, 200


@app.route("/health", methods=["GET"])
def health() -> tuple[dict, int]:
    """
    Health check endpoint.
    Used by monitoring systems (Kubernetes, load balancers).
    """
    app.logger.info("Health check accessed")
    return {"status": "healthy"}, 200


@app.route("/tickets", methods=["POST"])
def create_ticket() -> tuple[dict, int]:
    """
    Create a new ticket.
    Expects JSON payload: { "title": "string" }
    """

    data: dict = request.get_json()

    # Validate input
    if not data or "title" not in data:
        return {"error": "title is required"}, 400

    # Create ticket object
    ticket: dict[str, str | int] = {
        "id": len(tickets) + 1,
        "title": data["title"],
        "status": "open"
    }

    # Store in memory
    tickets.append(ticket)

    # Log creation event
    app.logger.info(f"Created ticket: {ticket}")

    return ticket, 201


@app.route("/tickets", methods=["GET"])
def list_tickets() -> tuple[list[dict], int]:
    """
    Return all tickets in memory.
    """
    return tickets, 200


if __name__ == "__main__":
    # Run development server
    app.run(host="0.0.0.0", port=5000, debug=True)