export const TOPIC_LIBRARY = {
  animal: {
    id: 'animal',
    title: 'Animals',
    subtitle: 'Tu vung ve dong vat',
    words: [
      {
        id: 'animal-cat',
        word: 'Cat',
        meaning: 'Con meo',
        example: 'The cat is sleeping on the sofa.',
        learned: true,
      },
      {
        id: 'animal-dog',
        word: 'Dog',
        meaning: 'Con cho',
        example: 'The dog runs very fast in the park.',
        learned: false,
      },
      {
        id: 'animal-elephant',
        word: 'Elephant',
        meaning: 'Con voi',
        example: 'An elephant is much bigger than a horse.',
        learned: false,
      },
      {
        id: 'animal-rabbit',
        word: 'Rabbit',
        meaning: 'Con tho',
        example: 'The rabbit likes to eat carrots.',
        learned: true,
      },
    ],
  },
  travel: {
    id: 'travel',
    title: 'Travel',
    subtitle: 'Giao tiep va di chuyen',
    words: [
      {
        id: 'travel-ticket',
        word: 'Ticket',
        meaning: 'Ve',
        example: 'Please show your ticket before boarding.',
        learned: false,
      },
      {
        id: 'travel-passport',
        word: 'Passport',
        meaning: 'Ho chieu',
        example: 'She forgot her passport at home.',
        learned: true,
      },
      {
        id: 'travel-airport',
        word: 'Airport',
        meaning: 'San bay',
        example: 'We arrived at the airport very early.',
        learned: false,
      },
      {
        id: 'travel-luggage',
        word: 'Luggage',
        meaning: 'Hanh ly',
        example: 'His luggage was too heavy to carry.',
        learned: false,
      },
    ],
  },
  family: {
    id: 'family',
    title: 'Family',
    subtitle: 'Gia dinh va cac moi quan he',
    words: [
      {
        id: 'family-mother',
        word: 'Mother',
        meaning: 'Me',
        example: 'My mother cooks dinner every evening.',
        learned: true,
      },
      {
        id: 'family-father',
        word: 'Father',
        meaning: 'Bo',
        example: 'Her father drives to work every day.',
        learned: false,
      },
      {
        id: 'family-brother',
        word: 'Brother',
        meaning: 'Anh trai em trai',
        example: 'My brother plays football after school.',
        learned: false,
      },
      {
        id: 'family-cousin',
        word: 'Cousin',
        meaning: 'Anh chi em ho',
        example: 'We visited our cousin last weekend.',
        learned: false,
      },
    ],
  },
  school: {
    id: 'school',
    title: 'School',
    subtitle: 'Hoc tap va lop hoc',
    words: [
      {
        id: 'school-teacher',
        word: 'Teacher',
        meaning: 'Giao vien',
        example: 'The teacher explained the lesson clearly.',
        learned: true,
      },
      {
        id: 'school-homework',
        word: 'Homework',
        meaning: 'Bai tap ve nha',
        example: 'I finished my homework before dinner.',
        learned: true,
      },
      {
        id: 'school-blackboard',
        word: 'Blackboard',
        meaning: 'Bang den',
        example: 'The answer is written on the blackboard.',
        learned: false,
      },
      {
        id: 'school-classmate',
        word: 'Classmate',
        meaning: 'Ban cung lop',
        example: 'My classmate helped me with the exercise.',
        learned: false,
      },
    ],
  },
  work: {
    id: 'work',
    title: 'Work',
    subtitle: 'Van phong va cong viec',
    words: [
      {
        id: 'work-meeting',
        word: 'Meeting',
        meaning: 'Cuoc hop',
        example: 'The meeting starts at nine in the morning.',
        learned: false,
      },
      {
        id: 'work-deadline',
        word: 'Deadline',
        meaning: 'Han chot',
        example: 'We need to finish this report before the deadline.',
        learned: false,
      },
      {
        id: 'work-manager',
        word: 'Manager',
        meaning: 'Quan ly',
        example: 'The manager approved our plan yesterday.',
        learned: true,
      },
      {
        id: 'work-salary',
        word: 'Salary',
        meaning: 'Luong',
        example: 'She receives her salary at the end of each month.',
        learned: false,
      },
    ],
  },
  music: {
    id: 'music',
    title: 'Music',
    subtitle: 'Am nhac va nhac cu',
    words: [
      {
        id: 'music-song',
        word: 'Song',
        meaning: 'Bai hat',
        example: 'This song is very easy to remember.',
        learned: true,
      },
      {
        id: 'music-guitar',
        word: 'Guitar',
        meaning: 'Dan guitar',
        example: 'He plays the guitar every evening.',
        learned: false,
      },
      {
        id: 'music-piano',
        word: 'Piano',
        meaning: 'Dan piano',
        example: 'She learned piano when she was five.',
        learned: false,
      },
      {
        id: 'music-drum',
        word: 'Drum',
        meaning: 'Trong',
        example: 'The drum beat was loud and powerful.',
        learned: false,
      },
      {
        id: 'music-singer',
        word: 'Singer',
        meaning: 'Ca si',
        example: 'The singer performed on a big stage.',
        learned: true,
      },
      {
        id: 'music-concert',
        word: 'Concert',
        meaning: 'Buoi hoa nhac',
        example: 'We went to a concert last weekend.',
        learned: false,
      },
    ],
  },
}

export function getTopicList() {
  return Object.values(TOPIC_LIBRARY).map((topic) => {
    const total = topic.words.length
    const learned = topic.words.filter((word) => word.learned).length

    return {
      id: topic.id,
      title: topic.title,
      subtitle: topic.subtitle,
      total,
      learned,
      progress: total > 0 ? Math.round((learned / total) * 100) : 0,
    }
  })
}

export function getTopicById(topicId) {
  return TOPIC_LIBRARY[topicId] ?? null
}

export function getDashboardMockData() {
  const topicRows = getTopicList()
  const total = topicRows.reduce((sum, topic) => sum + topic.total, 0)
  const learned = topicRows.reduce((sum, topic) => sum + topic.learned, 0)

  return {
    overall_progress: {
      total,
      learned,
      percentage: total > 0 ? (learned / total) * 100 : 0,
    },
    topic_progress: Object.fromEntries(
      topicRows.map((topic) => [
        topic.id,
        {
          total: topic.total,
          learned: topic.learned,
        },
      ])
    ),
  }
}
