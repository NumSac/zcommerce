package main

import (
	"net/http"
)

type RequestPayload struct {
	Action   string         `json:"action"`
	Auth     AuthPayload    `json:"auth,omitempty"`
	Products ProductPayload `json:"products,omitempty"`
}

type AuthPayload struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

type LogPayload struct {
	Name string `json:"name"`
	Data string `json:"data"`
}

type UserShopppingCartPayload struct {
	UserId    string `json:"userId"`
	ItemId    string `json:"itemId"`
	ItemCount int    `json:"itemCount"`
}

type ProductPayload struct {
	Category    []string `json:"category,omitempty"`
	PageSize    int      `json:"pageSize"`
	CurrentPage int      `json:"currentPage"`
}

func (app *Config) HandleSubmission(w http.ResponseWriter, r *http.Request) {
	var requestPayload RequestPayload

	err := app.readJSON(w, r, &requestPayload)
	if err != nil {
		_ = app.errorJSON(w, err)
		return
	}

	switch requestPayload.Action {
	case "auth":
		app.authenticate(w, requestPayload.Auth)

	case "products":
		app.queryProducts(w, requestPayload.Products)
	}
}

func (app *Config) authenticate(w http.ResponseWriter, a AuthPayload) {
	// Create json we'll send to the authentication-service
}

func (app *Config) queryProducts(w http.ResponseWriter, p ProductPayload) {

}
