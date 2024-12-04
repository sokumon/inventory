context('ToDo', () => {
    before(() => {
    cy.login('Administrator', 'admin');
    cy.visit('/desk');
    });
   
    it('creates a new todo', () => {
    cy.visit('/app/todo/new-todo-1');
    cy.fill_field('description', 'this is a test todo', 'Text Editor').blur();
    cy.get('.page-title').should('contain', 'Not Saved');
    cy.get('.primary-action').click();
    cy.visit('/desk#List/ToDo');
    cy.location('hash').should('eq', '/app/todo');
    cy.get('.list-row').should('contain', 'this is a test todo');
    });
   });
   