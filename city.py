from case import Case


class City:
    def __init__(self):
        self.grid = []
        self.marks_grid = []
        self.cases = []
        self.errors = []
        self.coffee_shops = []
        self.coffee_shops_amount = 0
        self.distances_amount = 0
        self.case_num = 0
        self.width = 0
        self.length = 0
        self.case_started = False
        self.current_case = None

    def parse(self, name):
        file = open(name, 'r')
        line_num = 0
        coffee_shop_num = 1
        distance_num = 1

        for line in file:
            line = line.split()
            line_num += 1

            if self.case_started:
                if coffee_shop_num <= self.coffee_shops_amount:
                    coffee_shop_num += 1
                    if self.line_is_correct(line, 2, line_num):
                        self.add_coffee_shop(line, line_num)
                elif distance_num <= self.distances_amount:
                    distance_num += 1
                    if self.current_case.status:
                        if self.line_is_correct(line, 1, line_num) == 1:
                            optimal_position = self.get_optimal_position(line)
                            self.current_case.add_optimal_position(optimal_position)
                else:
                    self.clear_variables()
            else:
                if self.line_is_correct(line, 4, line_num):
                    self.start_case(line)

    def start_case(self, line):
        self.width = int(line[0])
        self.length = int(line[1])
        self.coffee_shops_amount = int(line[2])
        self.distances_amount = int(line[3])

        self.fill_grid(self.grid)
        self.fill_grid(self.marks_grid)
        self.case_started = True
        self.case_num += 1
        self.current_case = Case(self.case_num)
        self.cases.append(self.current_case)

    def fill_grid(self, grid):
        del grid[:]
        for x in range(0, self.length + 1):
            locations = []
            for y in range(0, self.width + 1):
                locations.append(0)
            grid.append(locations)

    # def print_grid(self):
    #     for x in range(1, self.length + 1):
    #         for y in range(1, self.width + 1):
    #             print(self.marks_grid[x][y], end=' ')
    #         print()
    #     print()

    def line_is_correct(self, line, args_amount, line_num):
        if len(line) == args_amount:
            for arg in line:
                if arg.isdigit():
                    return True
                else:
                    self.errors.append('Error. All arguments must be Integer type. Line %d' % line_num)
                    self.current_case.status = False
                    return False
        else:
            self.errors.append('Error. City line must contain %d arguments. Line %d' % (args_amount, line_num))
            self.current_case.status = False
            return False

    def add_coffee_shop(self, line, line_num):
            dx = len(self.grid)
            dy = len(self.grid[0])

            x = int(line[0])
            y = int(line[1])

            if 0 < x <= dx and 0 < y <= dy:
                if self.grid[y][x] != -1:
                    self.grid[y][x] = -1
                    self.coffee_shops.append({'x': x, 'y': y})
                else:
                    self.current_case.add_error('Error. Coffee shops can not have same coordinates. Line %d' % line_num)
                    self.current_case.status = False
            else:
                self.current_case.add_error('Error. Wrong coffee shop coordinates. Line %d' % line_num)
                self.current_case.status = False

    def get_optimal_position(self, line):
        distance = int(line[0])
        self.mark_reachable_locations(distance)

        optimal_position = None
        max_reached = 0

        for i in range(1, self.length + 1):
            for j in range(1, self.width + 1):
                if self.marks_grid[i][j] > max_reached:
                    max_reached = self.marks_grid[i][j]
                    optimal_position = {'distance': distance, 'x': j, 'y': i}
                elif self.marks_grid[i][j] == max_reached != 0:
                    if j < optimal_position['x'] and i <= optimal_position['y']:
                        optimal_position = {'distance': distance, 'x': j, 'y': i}
        self.fill_grid(self.marks_grid)
        return optimal_position

    def mark_reachable_locations(self, distance):
        for coffee_shop in self.coffee_shops:
            x = coffee_shop['x']
            y = coffee_shop['y']

            for i in range(-distance, distance + 1):
                a = distance - abs(i) + 1
                for j in range(abs(i) - distance, a):
                    try:
                        if self.grid[y + i][x + j] != -1:
                            self.marks_grid[y + i][x + j] += 1
                    except IndexError:
                        pass

    def clear_variables(self):
        self.grid = []
        self.coffee_shops = []
        self.coffee_shops_amount = 0
        self.distances_amount = 0
        self.case_started = False
        self.width = 0
        self.length = 0

    def print_result(self):
        for case in self.cases:
            case.print()

        for error in self.errors:
            print(error)


if __name__ == '__main__':
    city = City()
    city.parse('test')
    city.print_result()





