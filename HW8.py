import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def get_restaurant_data(db_filename):
    """
    This function accepts the file name of a database as a parameter and returns a list of
    dictionaries. The key:value pairs should be the name, category, building, and rating
    of each restaurant in the database.
    """
    con = sqlite3.connect(db_filename)
    cur = con.cursor()

    list_dict = []
    cur.execute('SELECT restaurants.name, restaurants.rating, categories.category, buildings.building FROM restaurants JOIN categories ON restaurants.category_id = categories.id JOIN buildings ON restaurants.building_id = buildings.id')
    res = cur.fetchall()

    for name, rating, category_id, building_id in res:
        dictionary = {}
        dictionary['name'] = name
        dictionary['category'] = category_id
        dictionary['building'] = building_id
        dictionary['rating'] = rating
        list_dict.append(dictionary)

    return list_dict


def barchart_restaurant_categories(db_filename):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the counts of each category.
    """
    con = sqlite3.connect(db_filename)
    cur = con.cursor()

    cur.execute('SELECT categories.category, COUNT(restaurants.name) FROM categories JOIN restaurants ON restaurants.category_id = categories.id GROUP BY category ORDER BY COUNT(restaurants.name) ASC')
    res = cur.fetchall()

    dictionary = {}

    for category, count in res:
        dictionary[category] = count

    x = []
    y = []
    for category in dictionary.keys():
        x.append(category)
    for count in dictionary.values():
        y.append(count)

    fig, ax = plt.subplots()
    ax.barh(x,y)
    ax.set(xlabel='Restaurant Categories', ylabel='Number of Restaurants', title='Types of Restaurant on South University Ave')
    plt.tight_layout()

    plt.show()
    
    return dictionary

#EXTRA CREDIT
def highest_rated_category(db_filename):#Do this through DB as well
    """
    This function finds the average restaurant rating for each category and returns a tuple containing the
    category name of the highest rated restaurants and the average rating of the restaurants
    in that category. This function should also create a bar chart that displays the categories along the y-axis
    and their ratings along the x-axis in descending order (by rating).
    """
    con = sqlite3.connect(db_filename)
    cur = con.cursor()

    cur.execute('SELECT categories.category, AVG(restaurants.rating) FROM categories JOIN restaurants ON restaurants.category_id = categories.id GROUP BY category ORDER BY AVG(restaurants.rating) ASC')
    res = cur.fetchall()

    categories = []
    averages = []
    for category, avg in res:
        categories.append(category)
        avrg = round(avg,1)
        averages.append(avrg)
    
    tup = ((categories[-1]),(averages[-1]))
    
    fig, ax = plt.subplots()
    ax.barh(categories,averages)
    ax.set(xlabel='Ratings', ylabel='Categories', title='Average Restaurant Ratings by Category')
    plt.tight_layout()

    plt.show()
    
    return(tup)


#Try calling your functions here
def main():
    db_filename = 'South_U_Restaurants.db'
    get_restaurant_data(db_filename)
    barchart_restaurant_categories(db_filename)
    highest_rated_category(db_filename)


class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'name': 'M-36 Coffee Roasters Cafe',
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.best_category = ('Deli', 4.6)

    def test_get_restaurant_data(self):
        rest_data = get_restaurant_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, list)
        self.assertEqual(rest_data[0], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_barchart_restaurant_categories(self):
        cat_data = barchart_restaurant_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_highest_rated_category(self):
        best_category = highest_rated_category('South_U_Restaurants.db')
        self.assertIsInstance(best_category, tuple)
        self.assertEqual(best_category, self.best_category)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
