using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TestModuleSimulator.Writers
{
    public abstract class Writer
    {
        public abstract void Write(DateTime timestamp, string result);
    }
}
