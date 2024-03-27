import csv
from pathlib import Path

import tidalapi

class TidalFavoritesManager:
    def __init__(self, session: tidalapi.Session) -> None:
            self.session = session

    def save_favorites_to_csv(self, favorites: list, filepath: Path) -> None:
        """Save new favorites to a CSV file, avoiding duplicates."""
        existing_favorites = self._load_existing_favorites(filepath)

        # Ensure only unique IDs are stored 
        unique_favorites = [f for f in favorites if str(f.id) not in existing_favorites]

        self._write_new_favorites(unique_favorites, existing_favorites, filepath)

    def _load_existing_favorites(self, filepath: Path) -> set:
        """Load existing favorites from a CSV file into a set."""
        if not filepath.exists():
            return set()

        with filepath.open("r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            return {row[0] for row in reader}

    def _write_new_favorites(self, favorites: list, existing_favorites: set, filepath: Path) -> None:
        """Write new favorites to CSV file."""
        with filepath.open("a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for favorite in favorites:
                writer.writerow([favorite.id])

    def download_favorites(self) -> None:
        """Save all favorites categories to their respective CSV files."""
        favorites_dir = Path("tidal-favorites")
        favorites_dir.mkdir(exist_ok=True)

        categories = {
            "albums": self.session.user.favorites.albums,
            "tracks": self.session.user.favorites.tracks,
            "videos": self.session.user.favorites.videos,
            "artists": self.session.user.favorites.artists,
            "playlists": self.session.user.favorites.playlists,
        }

        for category, get_favorites_func in categories.items():
            favorites = get_favorites_func()  # Get favorites from Tidal
            category_path = favorites_dir / f"{category}.csv"
            self.save_favorites_to_csv(favorites, category_path)

    def upload_favorites(self, csv_data, filename):  # Accept CSV data (reader or iterable)
        errors = []
        favorite_type = self._determine_favorite_type(filename)  # Assuming you can use the row data
        for row in csv_data:
            try:
                getattr(self.session.user.favorites, f"add_{favorite_type}")(row[0])
            except Exception as e:
                errors.append(str(e))
        return errors

        
    def _determine_favorite_type(self, filename: str) -> str:
        """Determine the type of favorite based on the filename."""
        if "albums" in filename:
            return "album"
        elif "tracks" in filename:
            return "track"
        elif "artists" in filename:
            return "artist"
        elif "playlists" in filename:
            return "playlist"
        elif "videos" in filename:
            return "video"
        else:
            raise ValueError(f"Unknown favorite type based on file name: {filename}")