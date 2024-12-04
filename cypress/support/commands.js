// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
Cypress.Commands.add("login", (email, password) => {
	if (!email) {
		email = Cypress.config("testUser") || "Administrator";
	}
	if (!password) {
		password = Cypress.env("adminPassword");
	}
	// cy.session clears all localStorage on new login, so we need to retain the last route
	const session_last_route = window.localStorage.getItem("session_last_route");
	return cy
		.session([email, password] || "", () => {
			return cy.request({
				url: "/api/method/login",
				method: "POST",
				body: {
					usr: email,
					pwd: password,
				},
			});
		})
		.then(() => {
			if (session_last_route) {
				window.localStorage.setItem("session_last_route", session_last_route);
			}
		});
});
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })