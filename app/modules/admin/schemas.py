from pydantic import BaseModel

class SettingsCreate(BaseModel):
    site_name: str
    login_img_url: str
    hero_img_url: str | None = None
    hero_video_url: str | None = None


class SettingsResponse(SettingsCreate):
    id: int
    site_name: str
    login_img_url: str
    hero_img_url: str | None = None
    hero_video_url: str | None = None

    model_config = {"from_attributes": True}
