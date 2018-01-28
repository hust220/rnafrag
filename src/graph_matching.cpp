/**************************************************
 * Find the maximum common sub-graph between two graphs
 *
 * Author: Jian Wang (jianopt@ad.unc.edu)
 * Date: 10/17/2017
 *
 * Compile:
 *     g++ -std=c++14 graph_matching.cpp
 *
 **************************************************/

#include <vector>
#include <array>
#include <algorithm>
#include <iostream>

struct Graph {
    std::vector<int> vertices;
    std::vector<std::vector<int>> edges;
};

using Pair = std::array<int, 2>;
using Match = std::vector<Pair>;
using Matches = std::vector<Match>;

struct GraphMatching {
    Matches matches;
    Match match;
    const Graph &g1, &g2;
    int n1, n2;

    GraphMatching(const Graph &graph1, const Graph &graph2) : g1(graph1), g2(graph2) {
        n1 = g1.vertices.size();
        n2 = g2.vertices.size();

        set_conn();
        set_matches();
    }

private:
    using Conn = std::vector<std::vector<int>>;

    Conn m_conn1;
    Conn m_conn2;

    void malloc_conn(Conn &conn, int n) {
        conn.resize(n);
        for (int i = 0; i < n; i++) conn[i].resize(n, 0);
    }

    void set_conn(Conn &conn, const Graph &g) {
        for (auto && e : g.edges) {
            conn[e[0]][e[1]] = e[2];
            conn[e[1]][e[0]] = e[2];
        }
    }

    void set_conn() {
        malloc_conn(m_conn1, n1);
        malloc_conn(m_conn2, n2);

        set_conn(m_conn1, g1);
        set_conn(m_conn2, g2);
    }

    void set_matches() {
        bool flag = false;
        for (int i = 0; i < n1; i++) {
            for (int j = 0; j < n2; j++) {
                if (!in_match(match, i, j)) {
                    if (is_match(match, i, j)) {
                        flag = true;
                        match.push_back({i, j});
                        set_matches();
                        match.pop_back();
                    }
                }

            }
        }
        if (!flag) {
            std::sort(match.begin(), match.end(), [](const Pair &p1, const Pair &p2){return p1[0] < p2[0] || (p1[0] == p2[0] && p1[1] <= p2[1]);});
            if (!exists(match)) matches.push_back(match);
        }
    }

    bool exists(const Match &m) {
        for (auto &&match : matches) {
            if (equal(match, m)) return true;
        }
        return false;
    }

    bool equal(const Match &m1, const Match &m2) {
        if (m1.size() != m2.size()) return false;
        int n = m1.size();
        for (int i = 0; i < n; i++) {
            if (m1[i][0] != m2[i][0] || m1[i][1] != m2[i][1]) return false;
        }
        return true;
    }

    bool in_match(const Match &m, int i, int j) {
        return std::find_if(m.begin(), m.end(), [&i](const Pair &p){return p[0] == i;}) != m.end() ||
            std::find_if(m.begin(), m.end(), [&j](const Pair &p){return p[1] == j;}) != m.end();
    }

    bool is_match(const Match &m, int i, int j) {
        if (m.empty()) return true;

        bool flag = false;
        for (auto && p : m) {
            int a = m_conn1[p[0]][i];
            int b = m_conn2[p[1]][j];
            if (a != 0 && b != 0) {
                if (a != b) return false;
                else flag = true;
            }
        }
        return flag;
    }
};

std::vector<Match> match_graph(const Graph &g1, const Graph &g2) {
    return GraphMatching(g1, g2).matches;
}

int main() {
    Graph g1{{0, 1, 2}, {{0, 1, 1}, {0, 2, 1}, {1, 2, 2}}};
    Graph g2{{0, 1, 2, 3}, {{0, 3, 1}, {3, 2, 1}, {2, 1, 2}, {0, 2, 2}}};
    for (auto && match : match_graph(g1, g2)) {
        std::cout << "New Match:" << std::endl;
        for (auto && p : match) {
            std::cout << p[0] << '-' << p[1] << ' ';
        }
        std::cout << std::endl;
    }
}


