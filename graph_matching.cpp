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
#include <sstream>
#include <fstream>
#include <numeric>

template<typename T, typename U>
T lexical_cast(U && u) {
    std::stringstream stream;
    T t;

    stream << u;
    stream >> t;
    return t;
}

std::vector<std::string> string_tokenize(const std::string &str, const std::string &delimiters) {
    std::vector<std::string> tokens;
    auto lastPos = str.find_first_not_of(delimiters, 0);
    auto pos = str.find_first_of(delimiters, lastPos);
    while (std::string::npos != pos || std::string::npos != lastPos) {
        tokens.push_back(str.substr(lastPos, pos - lastPos));
        lastPos = str.find_first_not_of(delimiters, pos);
        pos = str.find_first_of(delimiters, lastPos);
    }
    return std::move(tokens);
}

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
    std::vector<int> v1, v2;
    std::vector<std::vector<int>> w1, w2;

    GraphMatching(const Graph &graph1, const Graph &graph2) : g1(graph1), g2(graph2) {
        n1 = g1.vertices.size();
        n2 = g2.vertices.size();

        malloc_conn(m_conn1, n1);
        malloc_conn(m_conn2, n2);

        set_conn(m_conn1, g1);
        set_conn(m_conn2, g2);

        set_matches();

        std::sort(matches.begin(), matches.end(), [](const Match &m1, const Match &m2){
            return m1.size() >= m2.size();
        });
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

    void set_matches() {
        bool flag = false;
        for (int i = 0; i < n1; i++) {
            if (match_filter1(match, i)) {
                for (int j = 0; j < n2; j++) {
                    if (match_filter2(match, j)) {
                        if (is_match(match, i, j)) {
                            flag = true;
                            match.push_back({i, j});
                            set_matches();
                            match.pop_back();
                        }
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

    bool match_filter1(const Match &m, int i) {
        if (m.empty()) return true;

        bool flag = false;
        for (auto &&p : m) {
            if (p[0] == i) return false;
            if (m_conn1[i][p[0]]) flag = true;
        }
        return flag;
    }

    bool match_filter2(const Match &m, int i) {
        if (m.empty()) return true;

        bool flag = false;
        for (auto &&p : m) {
            if (p[1] == i) return false;
            if (m_conn2[i][p[1]]) flag = true;
        }
        return flag;
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

std::vector<Match> graph_match(const Graph &g1, const Graph &g2) {
    return GraphMatching(g1, g2).matches;
}

void graph_print(const Graph &g) {
    std::cout << g.vertices.size();
    for (auto &&edge : g.edges) {
        std::cout << edge[0]+1 << edge[1]+1 << edge[2] << std::endl;
    }
}

Graph graph_read(std::string fn) {
    std::ifstream ifile(fn.c_str());
    std::string line;
    int l = 0;
    Graph g;
    while (ifile) {
        std::getline(ifile, line);
        auto &&v = string_tokenize(line, " ");
        if (l == 0) {
            int n = lexical_cast<int>(v[0]);
            g.vertices.resize(n);
            for (int i = 0; i < n; i++) g.vertices[i] = i;
        }
        else if (!v.empty()) {
            std::vector<int> edge;
            for (auto &&s : v) edge.push_back(lexical_cast<int>(s)-1);
            edge.back()++;
            g.edges.push_back(std::move(edge));
        }
        l++;
    }
    ifile.close();
    return std::move(g);
}

int main(int argc, char **argv) {
//    Graph g1{{0, 1, 2}, {{0, 1, 1}, {0, 2, 1}, {1, 2, 2}}};
//    Graph g2{{0, 1, 2, 3}, {{0, 3, 1}, {3, 2, 1}, {2, 1, 2}, {0, 2, 2}}};
    auto &&g1 = graph_read(argv[1]);
    auto &&g2 = graph_read(argv[2]);
    for (auto && match : graph_match(g1, g2)) {
        std::cout << "New Match:" << std::endl;
        for (auto && p : match) {
            std::cout << p[0] << '-' << p[1] << ' ';
        }
        std::cout << std::endl;
    }
}


