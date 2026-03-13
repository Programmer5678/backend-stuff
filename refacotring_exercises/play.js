

function printOwing(invoice) {
    
    console.log("***********************");
    console.log("**** Customer Owes ****");
    console.log("***********************");

    let outstanding = outstanding();
    
    // record due date
    assignDueDate(invoice)
    //print details
    console.log(`name: ${invoice.customer}`);
    console.log(`amount: ${outstanding}`);
    console.log(`due: ${invoice.dueDate.toLocaleDateString()}`);

    function outstanding(){
        let outstanding = 0;
        // calculate outstanding
        for (const o of invoice.orders) {
            outstanding += o.amount;
        }
        return outstanding;
    }

    function assignDueDate(){
        const today = Clock.today;
        invoice.dueDate = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 30);
    }
}