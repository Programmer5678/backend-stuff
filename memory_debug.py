from pympler import muppy, summary, asizeof
import gc

def print_memory_snapshot(top_n_lists=6, sample_items=6):
    """
    Prints a memory summary of all objects and shows the largest lists with sample items.
    NOT NECCASSERILY NEEDED FOR GENERAL DEBUGGING. in some cases memory leaks arent caused by lists.

    Args:
        top_n_lists (int): How many of the largest lists to show.
        sample_items (int): How many items from each list to print.
    """
    
    gc.disable() # Disable automatic garbage collection for accurate snapshot
    
    # Get all objects
    all_objects = muppy.get_objects()

    # Print summary of all object types
    sum1 = summary.summarize(all_objects)
    summary.print_(sum1)

    # Filter only lists
    lists = [obj for obj in all_objects if isinstance(obj, list)]

    # Sort lists by deep size
    lists_sorted = sorted(lists, key=asizeof.asizeof, reverse=True)

    print(f"\nTop {top_n_lists} largest lists by memory:")
    for i, l in enumerate(lists_sorted[:top_n_lists]):
        print(f"\nList #{i+1}:")
        print(f"  Deep size: {asizeof.asizeof(l)/1024:.2f} KB")
        print(f"  Length: {len(l)}")
        # Print first few items
        sample = l[:sample_items] if len(l) >= sample_items else l
        for j, item in enumerate(sample):
            print(f"    Item {j}: {repr(item)}")
            
    gc.enable() # Re-enable automatic garbage collection
