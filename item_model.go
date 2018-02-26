package main

import (
	"database/sql"
	"time"
)

type item struct {
	ID           int       `json:"id"`
	Name         string    `json:"name"`
	FoodType     string    `json:"food_type"`
	Store        string    `json:"store"`
	DateAdded    time.Time `json:"date_added"`
	DateModified time.Time `json:"date_modified"`
}

func (i *item) allItems(db *sql.DB) ([]item, error) {
	rows, err := db.Query(`
    SELECT
      id,
      name,
      food_type,
      store,
      date_added,
      date_modified
    FROM
      items`)

	if err != nil {
		return nil, err
	}

	defer rows.Close()

	items := []item{}

	for rows.Next() {
		var i item
		if err := rows.Scan(&i.ID, &i.Name, &i.FoodType, &i.Store, &i.DateAdded, &i.DateModified); err != nil {
			return nil, err
		}
		items = append(items, i)
	}
	return items, nil
}

func (i *item) getItemByID(db *sql.DB) error {
	return db.QueryRow(`
    SELECT
      id,
      name,
      food_type,
      store,
      date_added,
      date_modified
    FROM
      items
    WHERE
      id=$1`, i.ID).Scan(
		&i.ID,
		&i.Name,
		&i.FoodType,
		&i.Store,
		&i.DateAdded,
		&i.DateModified)
}

func (i *item) newEntry(db *sql.DB) error {
	err := db.QueryRow(`
    INSERT INTO items(
      name,
      food_type,
      store,
      date_added,
      date_modified)
    VALUES(
      $1,
      $2,
      $3,
      current_timestamp,
      current_timestamp)
    RETURNING
      id`,
		i.Name,
		i.FoodType,
		i.Store,
		i.DateAdded,
		i.DateModified).Scan(
		&i.ID)

	if err != nil {
		return err
	}

	return nil
}
