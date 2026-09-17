from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_from_activity():
    # Arrange
    activity_name = "Chess Club"
    participant_email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={participant_email}"
    )

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == (
        f"Unregistered {participant_email} from {activity_name}"
    )

    activities = client.get("/activities").json()
    assert participant_email not in activities[activity_name]["participants"]


def test_unregister_missing_participant_returns_404():
    # Arrange
    activity_name = "Chess Club"
    missing_email = "missing@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={missing_email}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in this activity"


def test_signup_for_activity_successfully_registers_student():
    # Arrange
    activity_name = "Soccer Club"
    new_email = "new-student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={new_email}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"

    activities = client.get("/activities").json()
    assert new_email in activities[activity_name]["participants"]

    # Cleanup
    client.delete(f"/activities/{activity_name}/unregister?email={new_email}")


def test_signup_for_activity_rejects_duplicate_registration():
    # Arrange
    activity_name = "Chess Club"
    existing_email = "daniel@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={existing_email}"
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
