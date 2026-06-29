import networkx as nx
import pandas as pd


class GraphBuilderV3:

    @staticmethod
    def build(rkg_df):

        print("======================================")
        print("GNDO GraphBuilder V3")
        print("======================================")

        G = nx.DiGraph()

        ##################################################
        # Build Nodes
        ##################################################

        for _, row in rkg_df.iterrows():

            req = row.get("requirement_id")
            ver = row.get("verification_id")
            test = row.get("test_id")
            fail = row.get("failure_id")
            change = row.get("change_id")

            chapter = row.get("chapter")
            
            if pd.notna(req):
    
                G.add_node(
                    str(req),
                    type="REQ",
                    label=str(req),
                    chapter=chapter
                )
                
            if pd.notna(ver):
    
                G.add_node(
                    str(ver),
                    type="VER",
                    label=str(ver),
                    chapter=chapter
                )
                
    
            if pd.notna(test):
    
                G.add_node(
                    str(test),
                    type="TEST",
                    label=str(test),
                    chapter=chapter
                )
                
    
            if pd.notna(fail):
    
                G.add_node(
                    str(fail),
                    type="FAIL",
                    label=str(fail),
                    chapter=chapter
                )
                
    
            if pd.notna(change):
    
                G.add_node(
                    str(change),
                    type="CHANGE",
                    label=str(change),
                    chapter=chapter
                )
    
            ##################################################
            # Requirement -> Verification
            ##################################################
            
            if (
                pd.notna(req)
                and
                pd.notna(ver)
            ):
            
                G.add_edge(
                    str(req),
                    str(ver),
                    relation="verified_by"
                )
    
            ##################################################
            # Verification -> Test
            ##################################################
            
            if (
                pd.notna(ver)
                and
                pd.notna(test)
            ):
            
                G.add_edge(
                    str(ver),
                    str(test),
                    relation="tested_by"
                )
    
            ##################################################
            # Test -> Failure
            ##################################################
            
            if (
                pd.notna(test)
                and
                pd.notna(fail)
            ):
            
                G.add_edge(
                    str(test),
                    str(fail),
                    relation="may_fail_as"
                )
    
            ##################################################
            # Requirement -> Failure
            ##################################################
            
            if (
                pd.notna(req)
                and
                pd.notna(fail)
            ):
            
                G.add_edge(
                    str(req),
                    str(fail),
                    relation="failure_mode"
                )
    
            ##################################################
            # Change -> Requirement
            ##################################################
            
            affected_req = row.get(
                "affected_requirement"
            )
            
            if (
                pd.notna(change)
                and
                pd.notna(affected_req)
            ):
            
                G.add_edge(
                    str(change),
                    str(affected_req),
                    relation="changes"
                )
    
            ##################################################
            # Requirement -> Verification
            ##################################################
            
            affected_ver = row.get(
                "affected_verification"
            )
            
            if (
                pd.notna(affected_req)
                and
                pd.notna(affected_ver)
            ):
            
                G.add_edge(
                    str(affected_req),
                    str(affected_ver),
                    relation="reverify"
                )
    
            ##################################################
            # Verification -> Test
            ##################################################
            
            affected_test = row.get(
                "affected_test"
            )
            
            if (
                pd.notna(affected_ver)
                and
                pd.notna(affected_test)
            ):
            
                G.add_edge(
                    str(affected_ver),
                    str(affected_test),
                    relation="retest"
                )
                
            print()
    
            print("--------------------------------------")
            print("Nodes Created :", G.number_of_nodes())
            print("Edges Created :", G.number_of_edges())
            print("--------------------------------------")
    
            print()
    
            print("======================================")
            print("GNDO GraphBuilder V3")
            print("======================================")
            print("Rows :", len(rkg_df))
            print()
    
            ##################################################
            # Validation
            ##################################################
            
            req_count = 0
            ver_count = 0
            test_count = 0
            fail_count = 0
            change_count = 0
        
        for _, attr in G.nodes(data=True):
        
            node_type = attr.get("type")
        
            if node_type == "REQ":
                req_count += 1
        
            elif node_type == "VER":
                ver_count += 1
        
            elif node_type == "TEST":
                test_count += 1
        
            elif node_type == "FAIL":
                fail_count += 1
        
            elif node_type == "CHANGE":
                change_count += 1
        
        print("======================================")
        print("Graph Summary")
        print("======================================")
        
        print("REQ    :", req_count)
        print("VER    :", ver_count)
        print("TEST   :", test_count)
        print("FAIL   :", fail_count)
        print("CHANGE :", change_count)
        
        print("--------------------------------------")
        
        print("Total Nodes :", G.number_of_nodes())
        print("Total Edges :", G.number_of_edges())
        
        print("======================================")

        return G

    ##################################################
    # Impact Graph
    ##################################################
    @staticmethod
    def build_impact_graph(row):

        G = nx.DiGraph()
    
        change = row.get("change_id")
    
        req = row.get("affected_requirement")
    
        ver = row.get("affected_verification")
    
        test = row.get("affected_test")
    
        fail = row.get("failure_id")
    
        chapter = row.get("chapter")

        ##################################################
        # CHANGE
        ##################################################
    
        if pd.notna(change):
    
            G.add_node(
                str(change),
                type="CHANGE",
                label=str(change),
                chapter=chapter
            )
    
        ##################################################
        # REQUIREMENT
        ##################################################
    
        if pd.notna(req):
    
            G.add_node(
                str(req),
                type="REQ",
                label=str(req),
                chapter=chapter
            )
    
        ##################################################
        # VERIFICATION
        ##################################################
    
        if pd.notna(ver):
    
            G.add_node(
                str(ver),
                type="VER",
                label=str(ver),
                chapter=chapter
            )
    
        ##################################################
        # TEST
        ##################################################
    
        if pd.notna(test):
    
            G.add_node(
                str(test),
                type="TEST",
                label=str(test),
                chapter=chapter
            )
    
        ##################################################
        # FAILURE
        ##################################################
    
        if pd.notna(fail):
    
            G.add_node(
                str(fail),
                type="FAIL",
                label=str(fail),
                chapter=chapter
            )
        ##################################################
        # CHANGE -> REQUIREMENT
        ##################################################
    
        if (
            pd.notna(change)
            and
            pd.notna(req)
        ):
    
            G.add_edge(
                str(change),
                str(req),
                relation="changes"
            )

        ##################################################
        # REQUIREMENT -> VERIFICATION
        ##################################################
    
        if (
            pd.notna(req)
            and
            pd.notna(ver)
        ):
    
            G.add_edge(
                str(req),
                str(ver),
                relation="verified_by"
            )

        ##################################################
        # VERIFICATION -> TEST
        ##################################################
    
        if (
            pd.notna(ver)
            and
            pd.notna(test)
        ):
    
            G.add_edge(
                str(ver),
                str(test),
                relation="tested_by"
            )

        ##################################################
        # TEST -> FAILURE
        ##################################################
    
        if (
            pd.notna(test)
            and
            pd.notna(fail)
        ):
    
            G.add_edge(
                str(test),
                str(fail),
                relation="failure_mode"
            )

        ##################################################
        # REQUIREMENT -> FAILURE
        ##################################################
    
        if (
            pd.notna(req)
            and
            pd.notna(fail)
        ):
    
            G.add_edge(
                str(req),
                str(fail),
                relation="causes"
            )

        print()
    
        print("Impact Graph")
    
        print("---------------------------")
    
        print("Nodes :", G.number_of_nodes())
    
        print("Edges :", G.number_of_edges())
    
        print("---------------------------")
    
        for u, v in G.edges():
    
            print(
                u,
                "->",
                v
            )

        return G
