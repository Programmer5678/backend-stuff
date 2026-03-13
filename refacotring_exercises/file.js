// province.js

// Producer class
class Producer {
    constructor(aProvince, data) {
        this._province = aProvince;
        this._name = data.name;
        this._cost = data.cost;
        this._production = data.production || 0;
    }

    get name() {
        return this._name;
    }

    get cost() {
        return this._cost;
    }

    set cost(arg) {
        this._cost = parseInt(arg);
    }

    get production() {
        return this._production;
    }

    set production(amountStr) {
        const amount = parseInt(amountStr);
        const newProduction = Number.isNaN(amount) ? 0 : amount;
        // Update province's total production
        this._province.totalProduction += newProduction - this._production;
        this._production = newProduction;
    }
}

// Province class
class Province {
    constructor(doc) {
        this._name = doc.name;
        this._producers = [];
        this._totalProduction = 0;
        this._demand = doc.demand;
        this._price = doc.price;

        doc.producers.forEach(d => this.addProducer(new Producer(this, d)));
    }

    addProducer(producer) {
        this._producers.push(producer);
        this._totalProduction += producer.production;
    }

    // Accessors
    get name() {
        return this._name;
    }

    get producers() {
        return this._producers.slice();
    }

    get totalProduction() {
        return this._totalProduction;
    }

    set totalProduction(arg) {
        this._totalProduction = arg;
    }

    get demand() {
        return this._demand;
    }

    set demand(arg) {
        this._demand = parseInt(arg);
    }

    get price() {
        return this._price;
    }

    set price(arg) {
        this._price = parseInt(arg);
    }

    // Derived calculations
    get shortfall() {
        return this._demand - this.totalProduction;
    }

    get satisfiedDemand() {
        return Math.min(this._demand, this.totalProduction);
    }

    get demandValue() {
        return this.satisfiedDemand * this._price;
    }

    get demandCost() {
        let remainingDemand = this._demand;
        let result = 0;

        this.producers
            .sort((a, b) => a.cost - b.cost)
            .forEach(p => {
                const contribution = Math.min(remainingDemand, p.production);
                remainingDemand -= contribution;
                result += contribution * p.cost;
            });

        return result;
    }

    get profit() {
        return this.demandValue - this.demandCost;
    }
}

// Sample data
function sampleProvinceData() {
    return {
        name: "Asia",
        producers: [
            { name: "Byzantium", cost: 10, production: 9 },
            { name: "Attalia", cost: 12, production: 10 },
            { name: "Sinope", cost: 10, production: 6 },
        ],
        demand: 30,
        price: 20
    };
}

// Simple test --> Province object only as its the main endpoint here.
// Usages:  create province and make sure data is as expected, change producer production, province price, demand and totalProduction and get correct values, so just design the before and afters and assert.
// also test for invalid demand/price/totalProduction
// set producer production


// Example usage
const asiaData = sampleProvinceData();
const asia = new Province(asiaData);

console.log(`Province: ${asia.name}`);
console.log(`Total Production: ${asia.totalProduction}`);
console.log(`Shortfall: ${asia.shortfall}`);
console.log(`Profit: ${asia.profit}`);

asia.producers[0].production = 20; // Update production
console.log(`\nAfter updating Byzantium production:`);
console.log(`Total Production: ${asia.totalProduction}`);
console.log(`Shortfall: ${asia.shortfall}`);
console.log(`Profit: ${asia.profit}`);
