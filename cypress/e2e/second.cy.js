describe('Item',() => {
    before(() =>{
        cy.login('Administrator', 'apple');
        cy.visit("/app/item")
    })
    it('Create a new item',async () => {
        cy.get(".primary-action").click()
        let test = await fetch("/api/method/inventory_management.api.get_meta_from_doctype?doctype=Item")
        let response = await test.json()
        let fields = response["message"]
        let pencil_code = Math.floor(1000 + Math.random() * 9000)
        let data = ["Pencil", "Apsara", "Long Pencil", `Pencil-${pencil_code}`,"WH-0001",100,2,200,"WH-0001",true]
        for(let i = 0; i < data.length; i++){
            if(fields[i] == "same_as_default_warehouse"){
                console.log(fields[i])
                cy.get(`input[data-fieldname=${fields[i]}]`).check()
            }
            if(fields[i] != "item_description" && fields[i] != "opening_stock_balance" && fields[i] != "same_as_default_warehouse"){
                cy.get(`input[data-fieldname=${fields[i]}]`).type(data[i])
            } 
            console.log(fields[i])

           
        }   
        cy.get('.primary-action').last().click()
    })
})