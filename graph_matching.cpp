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
#include <list>
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

    GraphMatching(const Graph &graph1, const Graph &graph2) : g1(graph1), g2(graph2) {
        parse_graph(g1, m_conn1, m_connected_vertices1, n1);
        parse_graph(g2, m_conn2, m_connected_vertices2, n2);

        for (ii = 0; ii < n1; ii++) {
            for (jj = 0; jj < n2; jj++) {
//                std::cout << ii << ' ' << jj << std::endl;
                match_push(ii, jj);
                set_matches();
                match_pop();
            }
        }

//        std::cout << "matches: " << matches.size() << std::endl;

        std::sort(matches.begin(), matches.end(), [](const Match &m1, const Match &m2){
            return m1.size() >= m2.size();
        });
    }

private:
    using Conn = std::vector<std::vector<int>>;
    using ConnVerts = std::vector<std::list<int>>;

    Conn m_conn1;
    Conn m_conn2;
    ConnVerts m_connected_vertices1;
    ConnVerts m_connected_vertices2;

    int ii, jj;
    int n1, n2;
    std::list<int> v1, v2;
    std::list<std::list<int>> all_added1, all_added2, all_erased1, all_erased2;

    void parse_graph(const Graph &g, Conn &conn, ConnVerts &v, int &n) {
        n = g.vertices.size();

        conn.resize(n);
        for (int i = 0; i < n; i++) conn[i].resize(n, 0);
        for (auto && e : g.edges) {
            conn[e[0]][e[1]] = e[2];
            conn[e[1]][e[0]] = e[2];
        }

        v.resize(n);
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (conn[i][j]) {
                    v[i].push_back(j);
                }
            }
        }
    }

    void match_push(int i, int j) {
        std::list<int> erased1, erased2, added1, added2;

//        std::cout << "match: ";
//        for (auto &&p : match) std::cout << p[0] << '-' << p[1] << ' ';
//        std::cout << std::endl;

        match.push_back({i, j});

        auto it = std::find(v1.begin(), v1.end(), i);
        if (it != v1.end()) {
            v1.erase(it);
            erased1.push_back(i);
        }
        all_erased1.push_back(std::move(erased1));

        it = std::find(v2.begin(), v2.end(), j);
        if (it != v2.end()) {
            v2.erase(it);
            erased2.push_back(j);
        }
        all_erased2.push_back(std::move(erased2));

        for (auto &&n : m_connected_vertices1[i]) {
            if (n >= ii && n != i) {
                if (std::find(v1.begin(), v1.end(), n) == v1.end() && 
                    std::find_if(match.begin(), match.end(), [&n](const Pair &p){
                        return p[0] == n;
                    }) == match.end())
                {
                    v1.push_back(n);
                    added1.push_back(n);
                }
            }
        }
        all_added1.push_back(std::move(added1));

        for (auto &&n : m_connected_vertices2[j]) {
            if (n >= jj && n != j) {
                if (std::find(v2.begin(), v2.end(), n) == v2.end() &&
                    std::find_if(match.begin(), match.end(), [&n](const Pair &p){
                        return p[1] == n;
                    }) == match.end())
                {
                    v2.push_back(n);
                    added2.push_back(n);
                }
            }
        }
        all_added2.push_back(std::move(added2));

    }

    template<typename T>
    void print_list(T &&v, std::string name) {
        std::cout << name << ':';
        for (auto &&i : v) {
            std::cout << ' ' << i;
        }
        std::cout << std::endl;
    }

    void match_pop() {
        auto &added1 = all_added1.back();
        auto &added2 = all_added2.back();
        auto &erased1 = all_erased1.back();
        auto &erased2 = all_erased2.back();

        for (auto &&i : added1) {
            v1.erase(std::find(v1.begin(), v1.end(), i));
        }
        for (auto &&i : erased1) {
            v1.push_back(i);
        }

//        print_list(v2, "v2 begin");
        for (auto &&i : added2) {
            v2.erase(std::find(v2.begin(), v2.end(), i));
        }
        for (auto &&i : erased2) {
            v2.push_back(i);
        }
//        print_list(v2, "v2 after");

        match.pop_back();
        all_added1.pop_back();
        all_erased1.pop_back();
        all_added2.pop_back();
        all_erased2.pop_back();
    }

    void set_matches() {
        bool flag = false;
//        print_list(v1, "v1");
//        print_list(v2, "v2");
        auto w1 = v1;
        auto w2 = v2;
        for (auto &&i : w1) {
            for (auto &&j : w2) {
//                std::cout << "i: " << i << ", j: " << j << std::endl;
                if (is_match(match, i, j)) {
                    flag = true;
                    match_push(i, j);
                    set_matches();
                    match_pop();
                }
            }
        }
        if (!flag) {
//            std::cout << "match size: " << match.size() << std::endl;
//            std::cout << "match: ";
//            for (auto &&p : match) std::cout << p[0] << '-' << p[1] << ' ';
//            std::cout << std::endl;
            if (match.size() > 2) {
                auto m = match;
                std::sort(m.begin(), m.end(), [](const Pair &p1, const Pair &p2){return p1[0] < p2[0] || (p1[0] == p2[0] && p1[1] <= p2[1]);});
                if (!exists(m)) matches.push_back(m);
            }
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


