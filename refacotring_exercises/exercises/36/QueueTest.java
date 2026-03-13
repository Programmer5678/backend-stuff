package exercises.36;



public void testQ() {
    Queue q = new Queue();

    ArrayList delegate = q.delegate();

    // delegate.add("E1");
    // delegate.add("E2");
    q.addRear("E1");
    q.addRear("E2");

    assertEquals("E1", q.removeFront() );
    assertEquals("E2", q.removeFront() );

    // assertEquals(0, delegate.size());
    assertEquals(0, q.size() );

}
