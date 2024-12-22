import re


class Validator:
    def __init__(self):
        pass

    def isValidCars(self, carId, carName, carCost, centerId):
        carIdRegex = r'[0-9]+'
        carNameRegex = r'([A-Za-z0-9]+( [A-Za-z0-9]+)+)'
        carCostRegex = r'[0-9]+'
        centerIdRegex = r'[0-9]+'
        if re.match(carIdRegex, carId) is None:
            return False
        if re.match(carNameRegex, carName) is None:
            return False
        if re.match(carCostRegex, carCost) is None:
            return False
        if re.match(centerIdRegex, centerId) is None:
            return False
        return True

    def isValidCenter(self, centerId, centerAddress, centerCity):
        centerIdRegex = r'[0-9]+'
        centerAddressRegex = r'([ул.а-яА-я]+([, 0-9]+)+)'
        centerCityRegex = r'([г. а-яА-я]+([-а-яА-я])+)'
        if re.match(centerIdRegex, centerId) is None:
            return False
        if re.match(centerAddressRegex, centerAddress) is None:
            return False
        if re.match(centerCityRegex, centerCity) is None:
            return False
        return True

    def isValidCustomers(self, customerId, customerName, customerBirthdate, customerPassport):
        customerIdRegex = r'[0-9]+'
        customerNameRegex = r'([а-яА-я]+[ а-яА-я]+[а-яА-я])+'
        customerBirthdateRegex = r'([0-9]+[-0-9]+)+'
        customerPassportRegex = r'[0-9]+'
        if re.match(customerIdRegex, customerId) is None:
            return False
        if re.match(customerNameRegex, customerName) is None:
            return False
        if re.match(customerBirthdateRegex, customerBirthdate) is None:
            return False
        if re.match(customerPassportRegex, customerPassport) is None:
            return False
        return True

    def isValidOrders(self, orderId, orderDate, carId, customerId):
        orderIdRegex = r'[0-9]+'
        orderDateRegex = r'([0-9]+[-0-9]+)+'
        carIdRegex = r'[0-9]'
        customerIdRegex = r'[0-9]'
        if re.match(orderIdRegex, orderId) is None:
            return False
        if re.match(orderDateRegex, orderDate) is None:
            return False
        if re.match(carIdRegex, carId) is None:
            return False
        if re.match(customerIdRegex, customerId) is None:
            return False
        return True