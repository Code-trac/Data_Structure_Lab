class Patient:
    def __init__(self, pid=0, name="", age=0):
        self.id = pid
        self.name = name
        self.age = age
        self.severity = 0
        self.visit_count = 0
        self.history_ref = ""


class Doctor:
    def __init__(self, did=0, name="", specialization=""):
        self.id = did
        self.name = name
        self.specialization = specialization


class SlotStatus:
    FREE = 0
    BOOKED = 1
    COMPLETED = 2


class SlotNode:
    def __init__(self, slot_id, start_time, end_time):
        self.slot_id = slot_id
        self.start_time = start_time
        self.end_time = end_time
        self.status = SlotStatus.FREE
        self.patient_id = -1
        self.next = None


class TokenType:
    ROUTINE = 0
    EMERGENCY = 1


class Token:
    def __init__(self, token_id=0, patient_id=0, doctor_id=0, slot_id=-1, ttype=TokenType.ROUTINE):
        self.token_id = token_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.slot_id = slot_id
        self.type = ttype


class EmergencyNode:
    def __init__(self, patient_id=0, severity_score=0, token_id=0):
        self.patient_id = patient_id
        self.severity_score = severity_score
        self.token_id = token_id


class CircularQueue:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.arr = [None] * capacity
        self.front = 0
        self.rear = -1
        self.count = 0

    def is_full(self):
        return self.count == self.capacity

    def is_empty(self):
        return self.count == 0

    def size(self):
        return self.count

    def enqueue(self, token):
        if self.is_full():
            print("Routine queue overflow")
            return False
        self.rear = (self.rear + 1) % self.capacity
        self.arr[self.rear] = token
        self.count += 1
        return True

    def dequeue(self):
        if self.is_empty():
            print("Routine queue underflow")
            return None
        t = self.arr[self.front]
        self.front = (self.front + 1) % self.capacity
        self.count -= 1
        return t

    def peek(self):
        if self.is_empty():
            return None
        return self.arr[self.front]

    def undo_enqueue(self):
        if self.count == 0:
            return None
        t = self.arr[self.rear]
        self.rear = (self.rear - 1 + self.capacity) % self.capacity
        self.count -= 1
        return t

    def undo_dequeue_front(self, token):
        if self.is_full():
            return False
        self.front = (self.front - 1 + self.capacity) % self.capacity
        self.arr[self.front] = token
        self.count += 1
        return True

    def print_queue(self):
        if self.is_empty():
            print("Routine queue empty")
            return
        print("Routine Queue (front -> rear): ", end="")
        idx = self.front
        for _ in range(self.count):
            t = self.arr[idx]
            print(f"{t.token_id}(P{t.patient_id},D{t.doctor_id})", end=" ")
            idx = (idx + 1) % self.capacity
        print()


class EmergencyMinHeap:
    def __init__(self):
        self.heap = []

    def is_empty(self):
        return len(self.heap) == 0

    def size(self):
        return len(self.heap)

    def parent(self, i):
        return (i - 1) // 2

    def left(self, i):
        return 2 * i + 1

    def right(self, i):
        return 2 * i + 2

    def heapify_up(self, i):
        while i != 0 and self.heap[self.parent(i)].severity_score > self.heap[i].severity_score:
            self.heap[i], self.heap[self.parent(i)] = self.heap[self.parent(i)], self.heap[i]
            i = self.parent(i)

    def heapify_down(self, i):
        n = len(self.heap)
        while True:
            l = self.left(i)
            r = self.right(i)
            smallest = i
            if l < n and self.heap[l].severity_score < self.heap[smallest].severity_score:
                smallest = l
            if r < n and self.heap[r].severity_score < self.heap[smallest].severity_score:
                smallest = r
            if smallest == i:
                break
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            i = smallest

    def insert(self, node):
        self.heap.append(node)
        self.heapify_up(len(self.heap) - 1)

    def get_min(self):
        if not self.heap:
            return None
        return self.heap[0]

    def extract_min(self):
        if not self.heap:
            print("No emergency patients")
            return None
        res = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        if self.heap:
            self.heapify_down(0)
        return res

    def remove_by_patient_id(self, patient_id):
        idx = -1
        for i, node in enumerate(self.heap):
            if node.patient_id == patient_id:
                idx = i
                break
        if idx == -1:
            return None
        removed = self.heap[idx]
        self.heap[idx] = self.heap[-1]
        self.heap.pop()
        if idx < len(self.heap):
            self.heapify_up(idx)
            self.heapify_down(idx)
        return removed

    def print_heap(self):
        if not self.heap:
            print("No emergency patients")
            return
        print("Emergency triage (min-heap): ", end="")
        for n in self.heap:
            print(f"[P{n.patient_id},sev={n.severity_score}]", end=" ")
        print()


class PatientHashTable:
    def __init__(self, capacity=211):
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]

    def hash_func(self, key):
        return key % self.capacity

    def upsert(self, patient):
        idx = self.hash_func(patient.id)
        bucket = self.table[idx]
        for i, p in enumerate(bucket):
            if p.id == patient.id:
                bucket[i] = patient
                return
        bucket.append(patient)

    def get(self, pid):
        idx = self.hash_func(pid)
        for p in self.table[idx]:
            if p.id == pid:
                return p
        return None

    def remove(self, pid):
        idx = self.hash_func(pid)
        bucket = self.table[idx]
        for i, p in enumerate(bucket):
            if p.id == pid:
                del bucket[i]
                return True
        return False

    def get_all_patients(self):
        res = []
        for bucket in self.table:
            for p in bucket:
                res.append(p)
        return res


class ActionType:
    REGISTER_PATIENT = 0
    BOOK_ROUTINE = 1
    EMERGENCY_IN = 2
    SERVE_PATIENT = 3
    CANCEL_SLOT = 4


class Action:
    def __init__(self, atype=ActionType.REGISTER_PATIENT):
        self.type = atype
        self.token_snapshot = None
        self.patient_id = -1
        self.doctor_id = -1
        self.slot_id = -1
        self.severity_score = 0


class UndoStack:
    def __init__(self):
        self.stack = []

    def is_empty(self):
        return len(self.stack) == 0

    def push(self, action):
        self.stack.append(action)

    def pop(self):
        if not self.stack:
            return None
        return self.stack.pop()


class HospitalSystem:
    def __init__(self):
        self.doctors = {}
        self.doctor_schedules = {}
        self.routine_queue = CircularQueue(200)
        self.emergency_heap = EmergencyMinHeap()
        self.patient_index = PatientHashTable(211)
        self.undo_stack = UndoStack()
        self.next_patient_id = 1
        self.next_doctor_id = 1
        self.next_slot_id = 1
        self.next_token_id = 1
        self.total_served = 0

    def add_doctor(self, name, spec):
        did = self.next_doctor_id
        self.next_doctor_id += 1
        self.doctors[did] = Doctor(did, name, spec)
        self.doctor_schedules[did] = None
        print(f"Doctor added. ID = {did}")
        return did

    def print_doctors(self):
        if not self.doctors:
            print("No doctors registered")
            return
        print("Doctors:")
        for did, d in self.doctors.items():
            print(f"ID: {did} | {d.name} ({d.specialization})")

    def schedule_add_slot(self, doctor_id, start, end):
        if doctor_id not in self.doctors:
            print("Invalid doctorId")
            return -1
        sid = self.next_slot_id
        self.next_slot_id += 1
        node = SlotNode(sid, start, end)
        node.next = self.doctor_schedules[doctor_id]
        self.doctor_schedules[doctor_id] = node
        print(f"Slot added for Doctor {doctor_id} | SlotId = {sid}")
        return sid

    def schedule_cancel_slot(self, slot_id):
        for doc_id, head in self.doctor_schedules.items():
            prev = None
            cur = head
            while cur:
                if cur.slot_id == slot_id:
                    if cur.status == SlotStatus.BOOKED:
                        print("Slot currently booked. Marking FREE")
                        cur.status = SlotStatus.FREE
                        cur.patient_id = -1
                    else:
                        if prev:
                            prev.next = cur.next
                        else:
                            self.doctor_schedules[doc_id] = cur.next
                        cur = None
                    print(f"Slot {slot_id} cancelled/removed")
                    act = Action(ActionType.CANCEL_SLOT)
                    act.slot_id = slot_id
                    act.doctor_id = doc_id
                    self.undo_stack.push(act)
                    return True
                prev = cur
                cur = cur.next
        print(f"SlotId {slot_id} not found")
        return False

    def print_schedule(self, doctor_id):
        if doctor_id not in self.doctor_schedules:
            print("No such doctor")
            return
        cur = self.doctor_schedules[doctor_id]
        print(f"Schedule for Doctor {doctor_id}:")
        while cur:
            status = "FREE"
            if cur.status == SlotStatus.BOOKED:
                status = f"BOOKED (P{cur.patient_id})"
            elif cur.status == SlotStatus.COMPLETED:
                status = "COMPLETED"
            print(f"SlotId {cur.slot_id} [{cur.start_time}-{cur.end_time}] {status}")
            cur = cur.next

    def find_free_slot(self, doctor_id):
        cur = self.doctor_schedules.get(doctor_id)
        while cur:
            if cur.status == SlotStatus.FREE:
                return cur
            cur = cur.next
        return None

    def register_patient(self):
        name = input("Enter patient name: ").strip()
        age = int(input("Enter age: ").strip())
        pid = self.next_patient_id
        self.next_patient_id += 1
        p = Patient(pid, name, age)
        self.patient_index.upsert(p)
        print(f"Patient registered. ID = {pid}")
        act = Action(ActionType.REGISTER_PATIENT)
        act.patient_id = pid
        self.undo_stack.push(act)
        return pid

    def print_patient(self, pid):
        p = self.patient_index.get(pid)
        if not p:
            print("No such patient")
            return
        print(f"Patient ID: {p.id}, Name: {p.name}, Age: {p.age}, Visits: {p.visit_count}")

    def book_routine_appointment(self):
        try:
            patient_id = int(input("Enter patientId: ").strip())
        except:
            print("Invalid input")
            return False
        p = self.patient_index.get(patient_id)
        if not p:
            print("Patient not found. Register first")
            return False
        try:
            doctor_id = int(input("Enter doctorId: ").strip())
        except:
            print("Invalid input")
            return False
        if doctor_id not in self.doctors:
            print("Doctor not found")
            return False
        slot = self.find_free_slot(doctor_id)
        if not slot:
            print("No FREE slots for this doctor")
            return False
        token_id = self.next_token_id
        self.next_token_id += 1
        t = Token(token_id, patient_id, doctor_id, slot.slot_id, TokenType.ROUTINE)
        if not self.routine_queue.enqueue(t):
            print("Failed to enqueue routine appointment")
            return False
        slot.status = SlotStatus.BOOKED
        slot.patient_id = patient_id
        p.visit_count += 1
        self.patient_index.upsert(p)
        print(f"Routine appointment booked. TokenId = {token_id} | SlotId = {slot.slot_id}")
        act = Action(ActionType.BOOK_ROUTINE)
        act.token_snapshot = t
        act.patient_id = patient_id
        act.doctor_id = doctor_id
        act.slot_id = slot.slot_id
        self.undo_stack.push(act)
        return True

    def emergency_in(self):
        try:
            patient_id = int(input("Enter patientId: ").strip())
        except:
            print("Invalid input")
            return False
        p = self.patient_index.get(patient_id)
        if not p:
            print("Patient not found. Register first")
            return False
        try:
            severity = int(input("Enter severity score (lower = more severe): ").strip())
        except:
            print("Invalid input")
            return False
        token_id = self.next_token_id
        self.next_token_id += 1
        node = EmergencyNode(patient_id, severity, token_id)
        self.emergency_heap.insert(node)
        p.severity = severity
        p.visit_count += 1
        self.patient_index.upsert(p)
        print(f"Emergency patient added to triage. TokenId = {token_id}, Severity = {severity}")
        act = Action(ActionType.EMERGENCY_IN)
        act.patient_id = patient_id
        act.severity_score = severity
        act.token_snapshot = Token(token_id, patient_id, -1, -1, TokenType.EMERGENCY)
        self.undo_stack.push(act)
        return True

    def get_slot_node(self, doctor_id, slot_id):
        cur = self.doctor_schedules.get(doctor_id)
        while cur:
            if cur.slot_id == slot_id:
                return cur
            cur = cur.next
        return None

    def serve_next(self):
        if not self.emergency_heap.is_empty():
            en = self.emergency_heap.extract_min()
            if not en:
                return False
            self.total_served += 1
            print(f"Serving EMERGENCY PatientId {en.patient_id} (Severity {en.severity_score})")
            act = Action(ActionType.SERVE_PATIENT)
            act.patient_id = en.patient_id
            act.severity_score = en.severity_score
            act.token_snapshot = Token(en.token_id, en.patient_id, -1, -1, TokenType.EMERGENCY)
            self.undo_stack.push(act)
            return True
        t = self.routine_queue.dequeue()
        if not t:
            print("No patients in queue")
            return False
        self.total_served += 1
        print(f"Serving ROUTINE PatientId {t.patient_id} for Doctor {t.doctor_id} | SlotId {t.slot_id}")
        slot = self.get_slot_node(t.doctor_id, t.slot_id)
        if slot:
            slot.status = SlotStatus.COMPLETED
        act = Action(ActionType.SERVE_PATIENT)
        act.token_snapshot = t
        act.patient_id = t.patient_id
        act.doctor_id = t.doctor_id
        act.slot_id = t.slot_id
        self.undo_stack.push(act)
        return True

    def undo_last(self):
        act = self.undo_stack.pop()
        if not act:
            print("Nothing to undo")
            return
        if act.type == ActionType.REGISTER_PATIENT:
            ok = self.patient_index.remove(act.patient_id)
            if ok:
                print(f"Undo: removed recently registered patient {act.patient_id}")
            else:
                print("Undo failed: patient not found")
        elif act.type == ActionType.BOOK_ROUTINE:
            removed = self.routine_queue.undo_enqueue()
            if not removed:
                print("Undo failed: could not reverse enqueue")
            else:
                slot = self.get_slot_node(act.doctor_id, act.slot_id)
                if slot:
                    slot.status = SlotStatus.FREE
                    slot.patient_id = -1
                print(f"Undo: cancelled booked routine appointment (Token {removed.token_id})")
        elif act.type == ActionType.EMERGENCY_IN:
            removed = self.emergency_heap.remove_by_patient_id(act.patient_id)
            if removed:
                print(f"Undo: removed emergency patient {act.patient_id} from triage")
            else:
                print("Undo failed: emergency patient not found in heap")
        elif act.type == ActionType.SERVE_PATIENT:
            if act.token_snapshot.type == TokenType.EMERGENCY:
                node = EmergencyNode(act.patient_id, act.severity_score, act.token_snapshot.token_id)
                self.emergency_heap.insert(node)
                self.total_served = max(0, self.total_served - 1)
                print(f"Undo: restored EMERGENCY patient {act.patient_id} to triage")
            else:
                ok = self.routine_queue.undo_dequeue_front(act.token_snapshot)
                if ok:
                    slot = self.get_slot_node(act.doctor_id, act.slot_id)
                    if slot:
                        slot.status = SlotStatus.BOOKED
                        slot.patient_id = act.patient_id
                    self.total_served = max(0, self.total_served - 1)
                    print(f"Undo: restored ROUTINE patient {act.patient_id} into front of queue")
                else:
                    print("Undo failed: routine queue full or invalid")
        elif act.type == ActionType.CANCEL_SLOT:
            print("Undo for slot cancel not fully implemented")

    def report_per_doctor(self):
        print("---- Per Doctor Pending Count & Next Slot ----")
        for doc_id, doc in self.doctors.items():
            cur = self.doctor_schedules.get(doc_id)
            pending = 0
            next_free = None
            next_booked = None
            while cur:
                if cur.status == SlotStatus.BOOKED:
                    pending += 1
                    if not next_booked:
                        next_booked = cur
                if cur.status == SlotStatus.FREE and not next_free:
                    next_free = cur
                cur = cur.next
            print(f"Doctor {doc_id} - {doc.name}")
            print(f"  Pending appointments: {pending}")
            if next_booked:
                print(f"  Next BOOKED slot: {next_booked.slot_id} [{next_booked.start_time}-{next_booked.end_time}] (P{next_booked.patient_id})")
            else:
                print("  No booked slots")
            if next_free:
                print(f"  Next FREE slot: {next_free.slot_id} [{next_free.start_time}-{next_free.end_time}]")
            else:
                print("  No free slots")

    def report_served_vs_pending(self):
        pending_routine = self.routine_queue.size()
        pending_emergency = self.emergency_heap.size()
        print("---- Served vs Pending Summary ----")
        print(f"Total served: {self.total_served}")
        print(f"Pending routine: {pending_routine}")
        print(f"Pending emergency: {pending_emergency}")
        print(f"Total pending: {pending_routine + pending_emergency}")

    def report_top_k_patients(self, k):
        print(f"---- Top-{k} Most Frequent Patients ----")
        all_patients = self.patient_index.get_all_patients()
        if not all_patients:
            print("No patients")
            return
        all_patients.sort(key=lambda p: p.visit_count, reverse=True)
        for i, p in enumerate(all_patients[:k]):
            print(f"{i+1}. ID {p.id} | {p.name} | Visits: {p.visit_count}")

    def print_state(self):
        print("=== CURRENT STATE SNAPSHOT ===")
        self.print_doctors()
        print("-----------------")
        for doc_id in self.doctors.keys():
            self.print_schedule(doc_id)
            print("-----------------")
        self.routine_queue.print_queue()
        self.emergency_heap.print_heap()
        print("==============================")

    def run_cli(self):
        while True:
            print("\n====== Hospital Appointment & Triage System ======")
            print("1. Register Patient")
            print("2. Add Doctor")
            print("3. Add Slot to Doctor")
            print("4. Book Slot (Routine Appointment)")
            print("5. Emergency In")
            print("6. Serve Next")
            print("7. Cancel Slot")
            print("8. Undo Last Action")
            print("9. Reports")
            print("10. Show Current State")
            print("0. Exit")
            choice = input("Choose: ").strip()
            if not choice.isdigit():
                print("Invalid choice")
                continue
            ch = int(choice)
            if ch == 0:
                print("Exiting")
                break
            elif ch == 1:
                self.register_patient()
            elif ch == 2:
                name = input("Enter doctor name: ").strip()
                spec = input("Enter specialization: ").strip()
                self.add_doctor(name, spec)
            elif ch == 3:
                try:
                    doc_id = int(input("Enter doctorId: ").strip())
                except:
                    print("Invalid input")
                    continue
                start = input("Enter slot startTime (e.g., 10:00): ").strip()
                end = input("Enter slot endTime (e.g., 10:15): ").strip()
                self.schedule_add_slot(doc_id, start, end)
            elif ch == 4:
                self.book_routine_appointment()
            elif ch == 5:
                self.emergency_in()
            elif ch == 6:
                self.serve_next()
            elif ch == 7:
                try:
                    slot_id = int(input("Enter slotId to cancel: ").strip())
                except:
                    print("Invalid input")
                    continue
                self.schedule_cancel_slot(slot_id)
            elif ch == 8:
                self.undo_last()
            elif ch == 9:
                print("---- Reports Menu ----")
                print("1. Per doctor pending + next slot")
                print("2. Served vs pending summary")
                print("3. Top-K frequent patients")
                rc = input("Choose: ").strip()
                if not rc.isdigit():
                    print("Invalid choice")
                    continue
                rc = int(rc)
                if rc == 1:
                    self.report_per_doctor()
                elif rc == 2:
                    self.report_served_vs_pending()
                elif rc == 3:
                    k = int(input("Enter K: ").strip())
                    self.report_top_k_patients(k)
                else:
                    print("Invalid report choice")
            elif ch == 10:
                self.print_state()
            else:
                print("Invalid choice")


if __name__ == "__main__":
    system = HospitalSystem()
    d1 = system.add_doctor("Dr. Sharma", "Cardiology")
    d2 = system.add_doctor("Dr. Mehta", "Orthopedics")
    system.schedule_add_slot(d1, "10:00", "10:15")
    system.schedule_add_slot(d1, "10:15", "10:30")
    system.schedule_add_slot(d2, "11:00", "11:15")
    system.run_cli()
