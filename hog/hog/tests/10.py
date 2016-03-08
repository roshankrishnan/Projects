test = {
  'name': 'Question 10',
  'points': 3,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> final_win_rate() >= 0.69
          True
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> try:
      ...     from utils import final_win_rate
      ... except ImportError:
      ...     from tests.utils import final_win_rate
      >>> print('\nFinal strategy win rate:', final_win_rate())
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> final_win_rate() >= 0.73
          True
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> try:
      ...     from utils import final_win_rate
      ... except ImportError:
      ...     from tests.utils import final_win_rate
      >>> print('\nFinal strategy win rate:', final_win_rate())
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> final_win_rate() >= 0.77
          True
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> try:
      ...     from utils import final_win_rate
      ... except ImportError:
      ...     from tests.utils import final_win_rate
      >>> print('\nFinal strategy win rate:', final_win_rate())
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}